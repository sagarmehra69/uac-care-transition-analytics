import streamlit as st
import plotly.express as px

from sklearn.ensemble import IsolationForest


def run_anomaly_detection(df_full, anomaly_col):

    anomaly_df = df_full[
        ['Date', anomaly_col]
    ].dropna().copy()

    iso = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    anomaly_df['anomaly'] = iso.fit_predict(
        anomaly_df[[anomaly_col]]
    )

    anomaly_df['status'] = anomaly_df[
        'anomaly'
    ].map({
        1: 'Normal',
        -1: 'Anomaly'
    })

    fig = px.scatter(
        anomaly_df,
        x='Date',
        y=anomaly_col,
        color='status',
        title=f'Anomalies in {anomaly_col}'
    )

    st.plotly_chart(fig, use_container_width=True)