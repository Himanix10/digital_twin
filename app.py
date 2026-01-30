import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import base64
from datetime import datetime
from io import BytesIO

import tensorflow as tf
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

from sklearn.preprocessing import MinMaxScaler

from utils.data_quality import compute_data_quality
from utils.fusion import fuse_sensors
from utils.anomaly import compute_anomalies_and_health

from models.linear_model import run_linear_regression
from models.random_forest import run_random_forest
from models.lstm_model import run_lstm
from models.autoencoder import run_autoencoder

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Hybrid Digital Twin",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= THEME =================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = st.session_state.theme == "dark"

BG = "#0f172a" if DARK else "#ffffff"
CARD = "#1e293b" if DARK else "#f8fafc"
TEXT = "#f1f5f9" if DARK else "#0f172a"
MUTED = "#94a3b8" if DARK else "#475569"
ACCENT = "#3b82f6"
SUCCESS = "#10b981"
WARNING = "#f59e0b"
CRITICAL = "#ef4444"

# ================= CSS (POP + GLOW RESTORED) =================
st.markdown(f"""
<style>
.stApp {{
    background:{BG};
    color:{TEXT};
}}

.section {{
    background:{CARD};
    border:1px solid #334155;
    border-radius:14px;
    padding:1.6rem;
    margin-bottom:1.6rem;
    transition: all .25s ease;
}}

.section:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(59,130,246,.18);
    border-color:{ACCENT};
}}

.kpi {{
    background:{CARD};
    border:1px solid #334155;
    border-radius:12px;
    padding:1.2rem;
    transition: all .25s ease;
}}

.kpi:hover {{
    transform: scale(1.03);
    box-shadow: 0 0 25px rgba(59,130,246,.35);
    border-color:{ACCENT};
}}

.kpi-value {{
    font-size:2rem;
    font-weight:700;
}}

.health-glow {{
    animation: pulse 1.8s infinite;
}}

@keyframes pulse {{
    0% {{ box-shadow: 0 0 10px rgba(239,68,68,.4); }}
    50% {{ box-shadow: 0 0 30px rgba(239,68,68,.8); }}
    100% {{ box-shadow: 0 0 10px rgba(239,68,68,.4); }}
}}

.stButton>button {{
    background:{ACCENT};
    color:white;
    border-radius:10px;
    padding:.7rem 1.4rem;
    font-weight:600;
    transition: all .2s ease;
}}

.stButton>button:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(59,130,246,.6);
}}

input, select {{
    transition: all .2s ease;
}}

input:focus, select:focus {{
    box-shadow: 0 0 15px rgba(59,130,246,.6);
    border-color:{ACCENT};
}}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ Controls")

    if st.button("🌗 Toggle Theme"):
        st.session_state.theme = "light" if DARK else "dark"
        st.rerun()

    st.divider()

    data_mode = st.radio("Data Source", ["Upload CSV Dataset", "Simulated Data"])
    model_type = st.selectbox("Model", ["Linear Regression", "Random Forest", "LSTM", "Autoencoder"])

    prediction_horizon = st.slider(
        "Prediction Horizon",
        1, 50, 10,
        disabled=(model_type == "Autoencoder")
    )

    health_threshold = st.slider("Health Threshold (%)", 50, 95, 75)
    anomaly_limit = st.slider("Anomaly Limit", 1, 50, 10)

    report_format = st.selectbox("Download Format", ["CSV", "JSON", "Text"])

# ================= HEADER =================
st.markdown("""
<div class="section">
<h1>Hybrid Digital Twin</h1>
<p>Industrial AI • Predictive Monitoring • Digital Twin Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ================= DATA =================
df = None
if data_mode == "Upload CSV Dataset":
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
else:
    df = pd.DataFrame({
        "temperature": 50 + np.random.randn(200),
        "vibration": 30 + np.random.randn(200),
        "pressure": 100 + np.random.randn(200)
    })

if df is None:
    st.stop()

numeric_df = df.select_dtypes(include=np.number)

# ================= SENSOR SELECTION =================
st.markdown('<div class="section">', unsafe_allow_html=True)
sensors = st.multiselect("Sensors", numeric_df.columns, default=list(numeric_df.columns[:2]))
st.markdown('</div>', unsafe_allow_html=True)

# ================= DATA QUALITY =================
dq = compute_data_quality(numeric_df, sensors)

st.markdown('<div class="section">', unsafe_allow_html=True)
cols = st.columns(4)
for c,l,v in zip(cols,
    ["Missing %","Noise","Outliers","Quality"],
    [f"{dq['missing_pct']:.1f}%",
     f"{dq['noise']:.2e}",
     f"{dq['outlier_pct']:.1f}%",
     f"{dq['quality_score']:.1f}%"]):
    c.markdown(f"<div class='kpi'><div>{l}</div><div class='kpi-value'>{v}</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================= MODEL =================
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

# ================= FUTURE =================
future = []
if model_type != "Autoencoder":
    future = np.full(prediction_horizon, predicted[-1])

# ================= HEALTH =================
anomalies, error, health = compute_anomalies_and_health(actual, predicted)
health = float(np.mean(health))

if health < health_threshold or len(anomalies) > anomaly_limit:
    status, color = "Critical", CRITICAL
elif health < health_threshold + 10:
    status, color = "Warning", WARNING
else:
    status, color = "Healthy", SUCCESS

# ================= HEALTH KPIs =================
st.markdown('<div class="section">', unsafe_allow_html=True)
c1,c2,c3 = st.columns(3)

glow = "health-glow" if status == "Critical" else ""

c1.markdown(f"<div class='kpi {glow}'><div>Health</div><div class='kpi-value' style='color:{color}'>{health:.1f}%</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='kpi'><div>Status</div><div class='kpi-value' style='color:{color}'>{status}</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='kpi'><div>Anomalies</div><div class='kpi-value'>{len(anomalies)}</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================= PLOT =================
st.markdown('<div class="section">', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(13,5))
ax.plot(actual, label="Actual")
ax.plot(predicted, '--', label="Predicted")

if len(future)>0:
    ax.plot(range(len(actual),len(actual)+len(future)), future, ':', label="Future")

if len(anomalies)>0:
    ax.scatter(anomalies, np.array(actual)[anomalies], color=CRITICAL)

ax.legend()
ax.grid(alpha=.2)
st.pyplot(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================= DOWNLOAD REPORT =================
report = {
    "timestamp": datetime.now().isoformat(),
    "model": model_type,
    "health": health,
    "status": status,
    "anomalies": len(anomalies),
    "prediction_horizon": prediction_horizon
}

buffer = BytesIO()
if report_format == "CSV":
    pd.DataFrame([report]).to_csv(buffer, index=False)
elif report_format == "JSON":
    buffer.write(json.dumps(report, indent=2).encode())
else:
    buffer.write("\n".join(f"{k}: {v}" for k,v in report.items()).encode())

b64 = base64.b64encode(buffer.getvalue()).decode()
st.markdown(f"""
<a href="data:application/octet-stream;base64,{b64}" download="digital_twin_report.{report_format.lower()}">
<button>⬇️ Download Report</button>
</a>
""", unsafe_allow_html=True)

# ================= FOOTER =================
st.caption("Hybrid Digital Twin • Pop + Glow UI • Prediction Horizon • MCP Ready")
