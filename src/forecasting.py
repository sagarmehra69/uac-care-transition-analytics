import numpy as np
import plotly.express as px
import streamlit as st

from prophet import Prophet
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)


def run_forecast_section(df_full, metric):

    if metric not in df_full.columns:
        st.warning("Selected metric not found.")
        return

    df_forecast = df_full[['Date', metric]].dropna()

    df_forecast = df_forecast.rename(
        columns={
            'Date': 'ds',
            metric: 'y'
        }
    )

    if len(df_forecast) < 30:
        st.warning("At least 30 data points are required for forecasting.")
        return

    model = Prophet()

    model.fit(df_forecast)

    future = model.make_future_dataframe(periods=30)

    forecast = model.predict(future)

    forecast_view = forecast[
        ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
    ].tail(30)

    fig_ci = px.line(
        forecast_view,
        x='ds',
        y=['yhat', 'yhat_lower', 'yhat_upper'],
        title='Forecast Confidence Interval'
    )

    st.plotly_chart(fig_ci, use_container_width=True)

    actual = df_forecast['y'].values
    predicted = forecast['yhat'][:len(actual)].values

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    mask = actual != 0

    if mask.any():
        mape = np.mean(
            np.abs(
                (actual[mask] - predicted[mask])
                / actual[mask]
            )
        ) * 100
    else:
        mape = 0

    m1, m2, m3 = st.columns(3)

    m1.metric("MAE", f"{mae:.4f}")
    m2.metric("RMSE", f"{rmse:.4f}")
    m3.metric("MAPE", f"{mape:.2f}%")

    fig = model.plot(forecast)

    fig.set_size_inches(8, 2)

    st.pyplot(fig)

    forecast_peak = forecast['yhat'].tail(30).max()

    if forecast_peak > df_forecast['y'].mean() * 1.20:
        st.error(
            "⚠️ Predicted operational surge detected."
        )
    else:
        st.success(
            "✅ No major capacity stress predicted."
        )