import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def render_dashboard():
    st.write("DEBUG: dashboard started")
    
    data_mode, model_type, horizon, health_threshold, anomaly_limit, report_format = render_sidebar()
    st.write("DEBUG: sidebar done")
    
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    st.write("DEBUG: markdown done")

    # ───────────────── DATA INPUT ─────────────────
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if data_mode == "Upload CSV Dataset":
            file = st.file_uploader("Upload time-series CSV", type=["csv"])
            df = pd.read_csv(file) if file is not None else None
        else:
            df = pd.DataFrame({
                "temperature": 50 + np.random.randn(200) * 5,
                "vibration":   30 + np.random.randn(200) * 3,
                "pressure":   100 + np.random.randn(200) * 8,
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
            (f"{dq['noise']:.2f}",         "Noise"),
            (f"{dq['outlier_pct']:.1f}%",  "Outliers"),
            (f"{dq['quality_score']:.1f}%","Quality Score"),
        ]
        for col, (value, label) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value-visible">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ───────────────── RUN MODEL BUTTON ─────────────────
    if "model_results" not in st.session_state:
        st.session_state.model_results = None

    if st.button("▶ Run Model", type="primary", use_container_width=True):
        fused = fuse_sensors(dq["filled_df"], sensors)
        scaler = MinMaxScaler()

        with st.spinner(f"Running {model_type}..."):
            if model_type == "Linear Regression":
                from models.linear_model import run_linear_regression
                actual = fused
                predicted = run_linear_regression(fused)
            elif model_type == "Random Forest":
                from models.random_forest import run_random_forest
                actual = fused
                predicted = run_random_forest(fused)
            elif model_type == "LSTM":
                from models.lstm_model import run_lstm
                actual, predicted = run_lstm(fused, scaler)
            else:
                from models.autoencoder import run_autoencoder
                actual, predicted = run_autoencoder(fused, scaler)

        anomalies, error, health = compute_anomalies_and_health(actual, predicted)
        health_val = float(np.mean(health))
        anomaly_count = len(anomalies)

        if health_val < health_threshold or anomaly_count > anomaly_limit:
            status = "Critical"
        elif health_val < health_threshold + 10:
            status = "Warning"
        else:
            status = "Healthy"

        st.session_state.model_results = {
            "actual": actual,
            "predicted": predicted,
            "anomalies": anomalies,
            "error": error,
            "health": health_val,
            "anomaly_count": anomaly_count,
            "status": status,
            "future": np.full(horizon, predicted[-1]),
            "noise": dq["noise"],
        }

    # ───────────────── SHOW RESULTS ─────────────────
    if st.session_state.model_results:
        r = st.session_state.model_results

        with st.container():
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("System Health & Forecast")
            cols = st.columns(3)
            with cols[0]: st.metric("Health Score", f"{r['health']:.1f}%")
            with cols[1]: st.metric("Status", r["status"])
            with cols[2]: st.metric("Detected Anomalies", r["anomaly_count"])

            fig = plot_system(r["actual"], r["predicted"], r["anomalies"], r["future"])
            st.pyplot(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        render_report_download(model_type, r["health"], r["status"], r["anomalies"], horizon, report_format)

        # ───────────────── AI EXPLAINER ─────────────────
        with st.container():
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("AI System Explanation")

            if st.button("Generate AI Explanation"):
                hybrid_prompt = f"health:{int(r['health'])}\nanomalies:{r['anomaly_count']}\nnoise:{int(r['noise'])}"
                with st.spinner("AI analyzing system state..."):
                    from ai.explainer import generate_explanation
                    explanation = generate_explanation(hybrid_prompt)
                st.text_area("AI Explanation Output", explanation, height=250)

            st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render_dashboard()