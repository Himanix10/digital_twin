import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from ui.sidebar import render_sidebar
from ui.plots import plot_system
from ui.reports import render_report_download

from utils.data_quality import compute_data_quality
from utils.fusion import fuse_sensors
from utils.anomaly import compute_anomalies_and_health

from models.linear_model import run_linear_regression
from models.random_forest import run_random_forest
from models.lstm_model import run_lstm
from models.autoencoder import run_autoencoder
from ai.explainer import generate_explanation


def render_dashboard():
    data_mode, model_type, horizon, health_threshold, anomaly_limit, report_format = render_sidebar()

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <h1 style='font-size: 2.9rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 0.5rem;'>
        Digital Twin Control Center
    </h1>
    <p style='color:#cbd5e1; font-size:1.15rem; margin-bottom:2.2rem;'>
        Real-time monitoring • Predictive analytics • Anomaly detection
    </p>
    """, unsafe_allow_html=True)

    # ───────────────── DATA INPUT ─────────────────
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

        if data_mode == "Upload CSV Dataset":
            file = st.file_uploader("Upload time-series CSV", type=["csv"])
            if file is not None:
                df = pd.read_csv(file)
            else:
                df = None
        else:
            df = pd.DataFrame({
                "temperature": 50 + np.random.randn(200) * 5,
                "vibration": 30 + np.random.randn(200) * 3,
                "pressure": 100 + np.random.randn(200) * 8,
            })
            st.caption("Using synthetic simulation data (200 timesteps)")

        st.markdown("</div>", unsafe_allow_html=True)

    if df is None:
        st.info("Please upload a CSV file to begin analysis.")
        return

    numeric_df = df.select_dtypes(include=np.number)

    sensors = st.multiselect(
        "Sensors to monitor",
        options=list(numeric_df.columns),
        default=list(numeric_df.columns[:min(3, len(numeric_df.columns))])
    )

    if not sensors:
        st.warning("Please select at least one sensor.")
        return

    # ───────────────── DATA QUALITY ─────────────────
    dq = compute_data_quality(numeric_df, sensors)

    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Data Quality Assessment")

        cols = st.columns(4)
        metrics = [
            (f"{dq['missing_pct']:.1f}%", "Missing"),
            (f"{dq['noise']:.2f}", "Noise"),
            (f"{dq['outlier_pct']:.1f}%", "Outliers"),
            (f"{dq['quality_score']:.1f}%", "Quality Score")
        ]

        for col, (value, label) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value-visible">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ───────────────── MODEL COMPUTATION ─────────────────
    fused = fuse_sensors(dq["filled_df"], sensors)
    scaler = MinMaxScaler()

    if model_type == "Linear Regression":
        actual = fused
        predicted = run_linear_regression(fused)
    elif model_type == "Random Forest":
        actual = fused
        predicted = run_random_forest(fused)
    elif model_type == "LSTM":
        actual, predicted = run_lstm(fused, scaler)
    else:
        actual, predicted = run_autoencoder(fused, scaler)

    anomalies, error, health = compute_anomalies_and_health(actual, predicted)

    error_value = float(np.mean(error))
    anomaly_count = len(anomalies)
    health = float(np.mean(health))

    if health < health_threshold or anomaly_count > anomaly_limit:
        status = "Critical"
    elif health < health_threshold + 10:
        status = "Warning"
    else:
        status = "Healthy"

    future = np.full(horizon, predicted[-1])

    # ───────────────── SYSTEM OVERVIEW ─────────────────
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("System Health & Forecast")

        cols = st.columns(3)

        with cols[0]:
            st.metric("Health Score", f"{health:.1f}%")

        with cols[1]:
            st.metric("Status", status)

        with cols[2]:
            st.metric("Detected Anomalies", anomaly_count)

        fig = plot_system(actual, predicted, anomalies, future)
        st.pyplot(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    render_report_download(model_type, health, status, anomalies, horizon, report_format)

    # ───────────────── AI ASSISTANT ─────────────────
   # st.markdown("### AI Assistant")
    #user_query = st.text_input("Ask about system status")

   # if user_query:
    #    reply = chatbot_response(
     #       user_query,
      #      health,
       #     anomaly_count,
        #    dq["noise"],
          #  status
        #)
        #st.write(reply)

    # ───────────────── AI EXPLAINER (HYBRID) ─────────────────
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("AI System Explanation")

        if st.button("Generate AI Explanation"):

            hybrid_prompt = f"""
            health:{int(health)}
            anomalies:{anomaly_count}
            noise:{int(dq['noise'])}
            """

            with st.spinner("AI analyzing system state..."):
                explanation = generate_explanation(hybrid_prompt)

            st.text_area("AI Explanation Output", explanation, height=250)

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render_dashboard()