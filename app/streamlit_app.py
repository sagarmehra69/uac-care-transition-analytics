import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

# ✅ FIX #1 & #2 — set_page_config MUST be the absolute first st.* call
st.set_page_config(
    page_title="UAC Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from PIL import Image

from sklearn.metrics import mean_absolute_error, mean_squared_error

try:
    from prophet import Prophet
    from sklearn.ensemble import IsolationForest
    import seaborn as sns
    import matplotlib.pyplot as plt
    ADVANCED_FEATURES_AVAILABLE = True
except ImportError:
    ADVANCED_FEATURES_AVAILABLE = False

from src.style import load_css
from src.ui_components import kpi_card
from src.forecasting import run_forecast_section
from src.anomaly_detection import run_anomaly_detection
from src.executive_summary import build_executive_summary
from src.data_loader import load_data, load_data_from_upload
from src.preprocessing import clean_data, filter_by_date, get_monthly_aggregates
from src.metrics import compute_kpis, kpi_summary, monthly_kpi_table
from src.bottleneck import detect_bottlenecks, get_bottleneck_summary, bottleneck_stats
from src.visualization import (
    HHS_In_Care, intake_discharge_chart, kpi_trends_chart,
    backlog_chart, bottleneck_heatmap, outcome_stability_chart, monthly_summary_chart,
)
from src.utils import generate_insights, generate_recommendations

# ✅ FIX #1 — Correct path resolution, no bare pd.read_csv at module level
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "HHS_Unaccompanied_Alien_Children_Program.csv"

# ─── Asset paths ────────────────────────────────────────────────────────────
LOGO_PATH = str(BASE_DIR / "assets" / "logo.png")
HERO_PATH = str(BASE_DIR / "assets" / "hero.jpg")


# ─── Cached helpers ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def cached_clean_data(df):
    return clean_data(df)

@st.cache_data(show_spinner=False)
def cached_compute_kpis(df):
    return compute_kpis(df)

@st.cache_data(show_spinner=False)
def cached_monthly_aggregates(df):
    return get_monthly_aggregates(df)


load_css()


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 UAC Analytics")
    st.image(LOGO_PATH, width=150, caption="U.S. Department of Health & Human Services")
    st.markdown("---")
    st.markdown("### 📂 Data Source")
    data_source = st.radio(
        "Select Data Source",
        ["Use bundled dataset", "Upload CSV"],
        label_visibility="collapsed"
    )

    raw_df = None
    if data_source == "Upload CSV":
        uploaded = st.file_uploader("Upload HHS UAC CSV", type=["csv"])
        if uploaded:
            try:
                raw_df = load_data_from_upload(uploaded)
                st.success("File loaded successfully")
            except Exception as e:
                st.error(f"{e}")
    else:
        if DATA_PATH.exists():
            try:
                raw_df = load_data(DATA_PATH)
                st.success("Bundled dataset loaded")
            except Exception as e:
                st.error(f"Failed to load bundled dataset: {e}")
        else:
            st.warning(f"Bundled dataset not found at: {DATA_PATH}")

    st.markdown("---")

    if raw_df is not None:
        df_clean = cached_clean_data(raw_df)
        st.markdown("### 📅 Date Range")
        min_d = df_clean["Date"].min().date()
        max_d = df_clean["Date"].max().date()
        start_date = st.date_input("Start", value=min_d, min_value=min_d, max_value=max_d)
        end_date   = st.date_input("End",   value=max_d, min_value=min_d, max_value=max_d)
        if start_date > end_date:
            st.error("Start date must be before end date.")
            st.stop()
        df_filtered = filter_by_date(df_clean, str(start_date), str(end_date))

        st.markdown("---")
        st.markdown("### ⚙️ KPI Thresholds")
        thresh_te = st.slider("Min Transfer Efficiency",     0.0, 1.0, 0.80, 0.05)
        thresh_de = st.slider("Min Discharge Effectiveness", 0.0, 0.5, 0.10, 0.01)
        thresh_tp = st.slider("Min Pipeline Throughput",     0.0, 2.0, 0.50, 0.05)

        st.markdown("---")
        st.markdown("### 🔧 Bottleneck Settings")
        sustained_n = st.slider("Sustained Bottleneck Threshold (days)", 1, 14, 3)
        st.markdown("---")
        st.caption(f"Showing: {start_date} to {end_date}")
        st.caption(f"Rows in view: {len(df_filtered):,}")


# ─── HEADER ──────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(LOGO_PATH, width=200, caption="U.S. Department of Health & Human Services")
    st.markdown('</div>', unsafe_allow_html=True)
with col_title:
    st.markdown("""
    <div style='padding:18px 0 10px'>
      <h1 style='color:#00D4FF;margin:0;font-size:3.2rem;'>
        UAC Care Transition Efficiency & Placement Outcome Analytics 📊
      </h1>
      <p style='color:#8A8FA8;margin:4px 0 0;font-size:.95rem;'>
        Operational intelligence dashboard · U.S. Dept. of Health & Human Services 🏛️
      </p>
    </div>""", unsafe_allow_html=True)

# Hero image
st.markdown('<div class="hero-image">', unsafe_allow_html=True)
st.image(HERO_PATH, width=1400,
         caption="Building a Stronger, Healthier America 🇺🇸", output_format="JPEG")
st.markdown('</div>', unsafe_allow_html=True)

if raw_df is None:
    st.info("Upload a CSV or select the bundled dataset from the sidebar to begin.")
    st.stop()


# ─── DATA PROCESSING ─────────────────────────────────────────────────────────

# 1. Rescue missing column from raw data
try:
    raw_care_candidates = [
        c for c in raw_df.columns
        if 'children in hhs care' in c.lower()
        or 'children currently in care' in c.lower()
    ]
    if raw_care_candidates:
        raw_care_col = raw_care_candidates[0]
        date_map = dict(zip(
            pd.to_datetime(raw_df['Date'], errors='coerce').dt.date,
            raw_df[raw_care_col]
        ))
        df_filtered['HHS_In_Care'] = (
            pd.to_datetime(df_filtered['Date']).dt.date.map(date_map)
        )
except Exception as e:
    st.warning(f"Column mapping issue detected: {e}")

# 2. Standardise column names
rename_map = {}
for col in df_filtered.columns:
    c_low = col.lower().strip()
    if 'children in hhs care' in c_low:
        rename_map[col] = 'HHS_In_Care'
    elif 'children discharged from hhs care' in c_low:
        rename_map[col] = 'HHS_Discharges'
    elif 'children apprehended and placed in cbp custody' in c_low:
        rename_map[col] = 'CBP_Apprehensions'
    elif 'children transferred out of cbp custody' in c_low:
        rename_map[col] = 'CBP_Transfers_Out'
df_filtered = df_filtered.rename(columns=rename_map)

# 3. Sort by date
if 'Date' in df_filtered.columns:
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date'])
    df_filtered = df_filtered.sort_values('Date').reset_index(drop=True)

# 4. Numeric cleaning & interpolation
for col in ['HHS_In_Care', 'HHS_Discharges', 'CBP_Apprehensions']:
    if col in df_filtered.columns:
        df_filtered[col] = pd.to_numeric(
            df_filtered[col].astype(str).str.replace(r'[^\d.]', '', regex=True),
            errors='coerce'
        )
        df_filtered[col] = df_filtered[col].interpolate(method='linear').ffill().bfill()

# 5. KPI calculation
df_kpi = cached_compute_kpis(df_filtered)

# 6. Safe discharge effectiveness
if 'HHS_In_Care' in df_kpi.columns and 'HHS_Discharges' in df_kpi.columns:
    hhs_in_care  = pd.to_numeric(df_kpi['HHS_In_Care'],   errors='coerce')
    hhs_discharges = pd.to_numeric(df_kpi['HHS_Discharges'], errors='coerce')
    df_kpi['Discharge_Effectiveness'] = np.where(
        (hhs_in_care > 0) & hhs_in_care.notna() & hhs_discharges.notna(),
        (hhs_discharges / hhs_in_care) * 100,
        np.nan
    )
    df_kpi['Discharge_Effectiveness'] = (
        df_kpi['Discharge_Effectiveness'].replace([np.inf, -np.inf], np.nan)
    )

# 7. Bottleneck detection
try:
    df_full = detect_bottlenecks(df_kpi, sustained_days=sustained_n)
except Exception:
    st.info("ℹ️ Bottleneck detection unavailable for this date range. Widening dates may help.")
    df_full = df_kpi.copy()
    for col in ["CBP_Bottleneck", "HHS_Bottleneck", "CBP_Sustained",
                "HHS_Sustained", "Critical_Alert", "Severity_Score", "Any_Bottleneck"]:
        if col not in df_full.columns:
            df_full[col] = 0

summary = kpi_summary(df_full)

if 'Discharge_Effectiveness' in df_full.columns:
    eff_vals  = df_full['Discharge_Effectiveness'].dropna()
    valid_eff = eff_vals[eff_vals > 0]
    summary["avg_discharge_eff"] = valid_eff.mean() if len(valid_eff) > 0 else 0.0

bn_sum  = bottleneck_stats(df_full)
monthly = cached_monthly_aggregates(df_full)

if 'Discharge_Effectiveness' in monthly.columns:
    monthly['Discharge_Effectiveness'] = monthly['Discharge_Effectiveness'].fillna(0)


# ─── KPI CARDS ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><b>📊 Key Performance Indicators</b></div>',
            unsafe_allow_html=True)

if st.button("🔄 Refresh Dashboard", help="Recalculate all metrics"):
    st.rerun()

c1, c2, c3, c4, c5 = st.columns(5)

kpi_card(c1, "Avg Transfer Efficiency",
         summary.get("avg_transfer_eff", 0), "{:.1%}",
         f"Target >= {thresh_te:.0%}",
         "#6BCB77" if (summary.get("avg_transfer_eff") or 0) >= thresh_te else "#FF6B6B", "📈")

kpi_card(c2, "Avg Discharge Effectiveness",
         summary.get("avg_discharge_eff", 0), "{:.2%}",
         f"Target >= {thresh_de:.0%}",
         "#6BCB77" if (summary.get("avg_discharge_eff") or 0) >= thresh_de else "#FF6B6B", "🏥")

kpi_card(c3, "Avg Pipeline Throughput",
         summary.get("avg_throughput", 0), "{:.1%}",
         f"Target >= {thresh_tp:.0%}",
         "#6BCB77" if (summary.get("avg_throughput") or 0) >= thresh_tp else "#FF6B6B", "⚡")

kpi_card(c4, "Current Backlog",
         summary.get("current_backlog", 0), "{:,}",
         "Most recent observation",
         "#FF6B6B" if summary.get("current_backlog", 0) > 0 else "#6BCB77", "📋")

kpi_card(c5, "Avg Stability Score",
         summary.get("avg_stability", 0), "{:.1f}",
         "7-day sigma of discharges", "#B197FC", "📊")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Apprehensions", f"{summary.get('total_apprehensions', 0):,}")
m2.metric("Total Discharges",    f"{summary.get('total_discharges', 0):,}")
m3.metric("Total CBP Transfers", f"{summary.get('total_transfers', 0):,}")
m4.metric("Peak Backlog",        f"{summary.get('peak_backlog', 0):,}",
          delta=f"on {summary.get('peak_backlog_date', 'N/A')}", delta_color="inverse")
st.markdown("---")


def safe_pct(val, decimals=1):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "N/A"
    return f"{val:.{decimals}%}"


# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", "📈 KPI Trends", "🚧 Bottleneck Analysis",
    "💡 Insights & Recommendations", "🤖 Advanced Analytics"
])

with tab1:
    st.markdown('<div class="section-header"><b>📈 Pipeline Load Overview</b></div>',
                unsafe_allow_html=True)
    df_chart = df_full.copy()
    if 'HHS_In_Care' in df_chart.columns:
        max_val = df_chart['HHS_In_Care'].max()
        if pd.notna(max_val) and max_val > 0:
            other_max = df_chart[['CBP_Apprehensions', 'HHS_Discharges']].max().max()
            df_chart['HHS_In_Care_Normalized'] = (
                df_chart['HHS_In_Care'] / max_val
            ) * other_max

    # ✅ FIX #3 — use_container_width=True on ALL charts
    st.plotly_chart(HHS_In_Care(df_chart), use_container_width=True)

    ca, cb_ = st.columns(2)
    with ca:
        st.markdown('<div class="section-header"><b>📥 Intake vs Discharge Trends</b></div>',
                    unsafe_allow_html=True)
        st.plotly_chart(intake_discharge_chart(df_full), use_container_width=True)
    with cb_:
        st.markdown('<div class="section-header"><b>📊 Backlog Accumulation Rate</b></div>',
                    unsafe_allow_html=True)
        st.plotly_chart(backlog_chart(df_full), use_container_width=True)

    st.markdown('<div class="section-header"><b>📅 Monthly Summary</b></div>',
                unsafe_allow_html=True)
    st.plotly_chart(monthly_summary_chart(monthly), use_container_width=True)

    st.markdown('<div class="section-header"><b>🎯 Outcome Stability Score</b></div>',
                unsafe_allow_html=True)
    st.plotly_chart(outcome_stability_chart(df_full), use_container_width=True)

with tab2:
    st.markdown('<div class="section-header"><b>📈 KPI Time Series (14-Day Rolling Avg)</b></div>',
                unsafe_allow_html=True)
    st.plotly_chart(kpi_trends_chart(df_full), use_container_width=True)
    st.markdown('<div class="section-header"><b>📅 Monthly KPI Table</b></div>',
                unsafe_allow_html=True)
    mkpi = monthly_kpi_table(df_full)
    st.dataframe(
        mkpi[["YearMonth", "Transfer_Efficiency", "Discharge_Effectiveness",
              "Pipeline_Throughput", "Backlog_Rate", "Outcome_Stability"]]
        .rename(columns={"YearMonth": "Month", "Transfer_Efficiency": "Transfer Eff.",
                         "Discharge_Effectiveness": "Discharge Eff.",
                         "Pipeline_Throughput": "Throughput",
                         "Backlog_Rate": "Backlog Rate", "Outcome_Stability": "Stability"})
        .set_index("Month"),
        use_container_width=True, height=420
    )

with tab3:
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("CBP Bottleneck Days",  f"{bn_sum.get('pct_cbp_bottleneck', 0):.1f}%")
    b2.metric("HHS Bottleneck Days",  f"{bn_sum.get('pct_hhs_bottleneck', 0):.1f}%")
    b3.metric("Sustained Periods",    f"{bn_sum.get('n_sustained_periods', 0):,} days")
    b4.metric("Critical Alerts",      f"{bn_sum.get('n_critical_alerts', 0):,} days")

    ch, cs = st.columns([3, 2])
    with ch:
        st.markdown('<div class="section-header"><b>🔥 Bottleneck Severity Heatmap</b></div>',
                    unsafe_allow_html=True)
        bn_heatmap = bottleneck_heatmap(df_full)
        bn_heatmap.update_traces(colorscale=[[0, "#0E1117"], [1, "#AF112E"]])
        st.plotly_chart(bn_heatmap, use_container_width=True)
    with cs:
        st.markdown('<div class="section-header"><b>📊 Severity Distribution</b></div>',
                    unsafe_allow_html=True)
        if "Severity_Score" in df_full.columns:
            fig_h = px.histogram(
                df_full["Severity_Score"].dropna(), nbins=20,
                color_discrete_sequence=["#AF112E"], template="plotly_dark"
            )
            fig_h.update_layout(
                paper_bgcolor="#0E1117", plot_bgcolor="#1A1D2E",
                showlegend=False, height=300, margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_h, use_container_width=True)

    st.markdown('<div class="section-header"><b>🚨 Flagged Bottleneck Periods (Top 200)</b></div>',
                unsafe_allow_html=True)
    bn_table = get_bottleneck_summary(df_full).head(200)
    if len(bn_table):
        bn_display = bn_table.copy()
        bn_display["Date"] = bn_display["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(bn_display, use_container_width=True, height=420)
    else:
        st.info("No bottleneck periods detected in the selected date range.")

with tab4:
    ci, cr = st.columns(2)
    with ci:
        st.markdown('<div class="section-header"><b>💡 Auto-Generated Operational Insights</b></div>',
                    unsafe_allow_html=True)
        for ins in generate_insights(summary, bn_sum):
            st.markdown(f'<div class="insight-card">{ins}</div>', unsafe_allow_html=True)
    with cr:
        st.markdown('<div class="section-header"><b>🎯 Strategic Recommendations</b></div>',
                    unsafe_allow_html=True)
        for rec in generate_recommendations(summary, bn_sum):
            st.markdown(f"""<div class="rec-card">
              <b>{rec['priority']}</b> | <b>{rec['area']}</b><br>
              <span style='color:#C0C0D0'>{rec['action']}</span></div>""",
                        unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="section-header"><b>📋 Executive Summary Snapshot</b></div>',
                unsafe_allow_html=True)
    exec_text = f"""**Period:** {start_date} to {end_date}

**KPIs:** Transfer Efficiency: {safe_pct(summary.get('avg_transfer_eff'))} | Discharge Effectiveness: {safe_pct(summary.get('avg_discharge_eff'), 2)} | Throughput: {safe_pct(summary.get('avg_throughput'))}
**Backlog:** Current: {summary.get('current_backlog', 0):,} | Peak: {summary.get('peak_backlog', 0):,} on {summary.get('peak_backlog_date', 'N/A')}
**Bottlenecks:** CBP: {bn_sum.get('pct_cbp_bottleneck', 0):.1f}% | HHS: {bn_sum.get('pct_hhs_bottleneck', 0):.1f}% | Sustained: {bn_sum.get('n_sustained_periods', 0):,} days | Critical Alerts: {bn_sum.get('n_critical_alerts', 0):,}"""

    st.markdown(exec_text)
    st.download_button("📥 Download Executive Summary", data=exec_text,
                       file_name="executive_summary_snapshot.md", mime="text/markdown")

    with st.expander("📊 View Raw Processed Data"):
        st.dataframe(df_full.head(500), use_container_width=True)
        st.download_button("📥 Download Full Processed CSV",
                           data=df_full.to_csv(index=False).encode("utf-8"),
                           file_name="uac_processed.csv", mime="text/csv")

    # ✅ FIX #4 — entire advanced block inside the if, correct indentation
    if ADVANCED_FEATURES_AVAILABLE:
        st.markdown('<div class="section-header"><b>🔮 Time Series Forecasting</b></div>',
                    unsafe_allow_html=True)
        forecast_metric = st.selectbox(
            "Select Metric to Forecast",
            ["Discharge_Effectiveness", "Backlog_Rate", "Transfer_Efficiency"]
        )
        run_forecast_section(df_full, forecast_metric)

        st.markdown('<div class="section-header"><b>🔍 Anomaly Detection</b></div>',
                    unsafe_allow_html=True)
        numeric_cols = df_full.select_dtypes(include=[np.number]).columns
        anomaly_col = st.selectbox("Select Column for Anomaly Detection", numeric_cols)
        run_anomaly_detection(df_full, anomaly_col)

        st.markdown('<div class="section-header"><b>⚖️ Comparative Analysis</b></div>',
                    unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📅 Period 1")
            start1 = st.date_input("Start Date 1", value=min_d, key="start1")
            end1   = st.date_input("End Date 1",   value=max_d, key="end1")
        with col2:
            st.subheader("📅 Period 2")
            start2 = st.date_input("Start Date 2", value=min_d, key="start2")
            end2   = st.date_input("End Date 2",   value=max_d, key="end2")

        if st.button("🔍 Compare"):
            df1      = filter_by_date(df_clean, str(start1), str(end1))
            df1_kpi  = cached_compute_kpis(df1)
            summary1 = kpi_summary(df1_kpi)
            df2      = filter_by_date(df_clean, str(start2), str(end2))
            df2_kpi  = cached_compute_kpis(df2)
            summary2 = kpi_summary(df2_kpi)
            comp_df  = pd.DataFrame({
                'Metric': ['Avg Transfer Efficiency', 'Avg Discharge Effectiveness',
                           'Avg Pipeline Throughput', 'Current Backlog', 'Avg Stability Score'],
                'Period 1': [summary1.get("avg_transfer_eff", 0),
                             summary1.get("avg_discharge_eff", 0),
                             summary1.get("avg_throughput", 0),
                             summary1.get("current_backlog", 0),
                             summary1.get("avg_stability", 0)],
                'Period 2': [summary2.get("avg_transfer_eff", 0),
                             summary2.get("avg_discharge_eff", 0),
                             summary2.get("avg_throughput", 0),
                             summary2.get("current_backlog", 0),
                             summary2.get("avg_stability", 0)],
            })
            st.dataframe(comp_df)
            st.download_button("📥 Download Comparison CSV",
                               data=comp_df.to_csv(index=False).encode("utf-8"),
                               file_name="comparison.csv", mime="text/csv")
    else:
        st.info("Advanced features require `prophet` and `scikit-learn`. "
                "Add them to requirements.txt to enable forecasting and anomaly detection.")