import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)


def run_forecast_section(df_full, metric):

    if not PROPHET_AVAILABLE:
        st.info("⏳ Forecasting unavailable — prophet not installed.")
        return

    if metric not in df_full.columns:
        st.warning("Selected metric not found.")
        return

    df_forecast = df_full[['Date', metric]].dropna()
    df_forecast = df_forecast.rename(columns={'Date': 'ds', metric: 'y'})

    # Ensure ds is datetime, y is numeric
    df_forecast['ds'] = pd.to_datetime(df_forecast['ds'])
    df_forecast['y'] = pd.to_numeric(df_forecast['y'], errors='coerce')
    df_forecast = df_forecast.dropna()

    if len(df_forecast) < 30:
        st.warning("At least 30 data points are required for forecasting.")
        return

    try:
        # Force cmdstanpy backend — required on Streamlit Cloud
        model = Prophet(
            uncertainty_samples=100,
            stan_backend="CMDSTANPY"
        )
        model.fit(df_forecast)

        future   = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        forecast_view = forecast[
            ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
        ].tail(30)

        fig_ci = px.line(
            forecast_view,
            x='ds',
            y=['yhat', 'yhat_lower', 'yhat_upper'],
            title='Forecast Confidence Interval',
            template='plotly_dark'
        )
        st.plotly_chart(fig_ci, use_container_width=True)

        actual    = df_forecast['y'].values
        predicted = forecast['yhat'][:len(actual)].values

        mae  = mean_absolute_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mask = actual != 0
        mape = np.mean(
            np.abs((actual[mask] - predicted[mask]) / actual[mask])
        ) * 100 if mask.any() else 0

        m1, m2, m3 = st.columns(3)
        m1.metric("MAE",  f"{mae:.4f}")
        m2.metric("RMSE", f"{rmse:.4f}")
        m3.metric("MAPE", f"{mape:.2f}%")

        fig = model.plot(forecast)
        fig.set_size_inches(8, 2)
        st.pyplot(fig)

        forecast_peak = forecast['yhat'].tail(30).max()
        if forecast_peak > df_forecast['y'].mean() * 1.20:
            st.error("⚠️ Predicted operational surge detected.")
        else:
            st.success("✅ No major capacity stress predicted.")

    except Exception as e:
        st.error(f"Forecasting failed: {e}")
        st.info("Try selecting a different metric or widening the date range.")