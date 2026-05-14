import pandas as pd


def kpi_card(col, label, value, fmt, sub, color, emoji):

    if value is None or pd.isna(value):
        display_value = "N/A"
    else:
        display_value = fmt.format(value)

    col.markdown(f'''
    <div class="kpi-card">
      <div class="kpi-label">{emoji} {label}</div>
      <div class="kpi-value" style="color:{color};">{display_value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>
    ''', unsafe_allow_html=True)