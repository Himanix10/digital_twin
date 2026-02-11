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

def render_dashboard():
    data_mode, model_type, horizon, health_threshold, anomaly_limit, report_format = render_sidebar()

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <h1 style='
        font-size: 2.9rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    '>
        Digital Twin Control Center
    </h1>
    <p style='color:#cbd5e1; font-size:1.15rem; margin-bottom:2.2rem;'>
        Real-time monitoring • Predictive analytics • Anomaly detection
    </p>
    """, unsafe_allow_html=True)

    # ────────────────────────────────────────────────────────────────
    #   DATA INPUT SECTION
    # ────────────────────────────────────────────────────────────────
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

        if data_mode == "Upload CSV Dataset":
            file = st.file_uploader(
                "Upload time-series CSV",
                type=["csv"],
                help="Expected format: timestamp + numeric sensor columns"
            )
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
        default=list(numeric_df.columns[:min(3, len(numeric_df.columns))]),
        key="sensors_multiselect"
    )

    if not sensors:
        st.warning("Please select at least one sensor to continue.")
        return

    # ────────────────────────────────────────────────────────────────
    #   DATA QUALITY
    # ────────────────────────────────────────────────────────────────
    dq = compute_data_quality(numeric_df, sensors)

    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Data Quality Assessment")

        cols = st.columns(4)

        metrics = [
            (f"{dq['missing_pct']:.1f}%", "Missing"),
            (f"{dq['noise']:.2e}",       "Noise"),
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

    # ────────────────────────────────────────────────────────────────
    #   MODEL + ANOMALY COMPUTATION
    # ────────────────────────────────────────────────────────────────
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
    health = float(np.mean(health))

    if health < health_threshold or len(anomalies) > anomaly_limit:
        status = "Critical"
    elif health < health_threshold + 10:
        status = "Warning"
    else:
        status = "Healthy"

    future = np.full(horizon, predicted[-1])

    # ────────────────────────────────────────────────────────────────
    #   SYSTEM HEALTH OVERVIEW – ALIGNED VERSION
    # ────────────────────────────────────────────────────────────────
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

        st.subheader("System Health & Forecast")

        cols = st.columns(3, gap="medium", vertical_alignment="center")

        # Health Score
        with cols[0]:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value-visible">{health:.1f}%</div>
                <div class="metric-label">Health Score</div>
            </div>
            """, unsafe_allow_html=True)

        # Status (centered)
        with cols[1]:
            st.markdown(f"""
            <div class="metric-container">
                <div class="status-pill status-{status.lower()}" style="margin-bottom: 1rem;">{status}</div>
                <div class="metric-label">Current Status</div>
            </div>
            """, unsafe_allow_html=True)

        # Anomalies
        with cols[2]:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value-visible">{len(anomalies)}</div>
                <div class="metric-label">Detected Anomalies</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

        st.caption(f"**Model** • {model_type}  **•**  **Prediction Horizon** • {horizon} steps")

        fig = plot_system(actual, predicted, anomalies, future)
        st.pyplot(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Report download
    render_report_download(model_type, health, status, anomalies, horizon, report_format)