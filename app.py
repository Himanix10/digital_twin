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

# Compatibility helper for setting query params across Streamlit versions
def set_query_params(**kwargs):
    try:
        # Prefer the newer API: assign to st.query_params when available
        if hasattr(st, "query_params"):
            qp = dict(st.query_params) if isinstance(st.query_params, dict) else dict(st.query_params)
            # normalize values to lists of strings (query params are list-valued)
            for k, v in kwargs.items():
                qp[k] = [str(v)] if not isinstance(v, (list, tuple)) else [str(x) for x in v]
            try:
                st.query_params = qp
                return
            except Exception:
                # fall through to experimental API if assignment fails
                pass

        # Fallback for older Streamlit versions
        if hasattr(st, "experimental_set_query_params"):
            st.experimental_set_query_params(**{k: v for k, v in kwargs.items()})
    except Exception:
        # best-effort; don't crash the app for query param updates
        return
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
BG = "#0a0a0a" 
CARD = "#1a1a1a"
TEXT = "#fafafa" 
MUTED = "#a3a3a3"
ACCENT = "#fafafa" 
SUCCESS = "#fafafa"
WARNING = "#fafafa"
CRITICAL = "#fafafa"

# ================= CSS (POP + GLOW RESTORED) =================
st.markdown(f"""
<style>
:root {{
  --bg: {BG};
  --card: {CARD};
  --text: {TEXT};
  --muted: {MUTED};
  --accent: {ACCENT};
  --border: rgba(16,24,40,0.06);
}}
.stApp {{
    background:var(--bg);
    color:var(--text);
    font-family: Inter, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    padding:18px 22px;
}}

/* Sidebar container (target core attribute) */
[data-testid="stSidebar"] > div:first-child {{
    background: #1a1a1a;
    border-right: 1px solid #333;
    padding: 24px;
    color: #fafafa;
}}

/* File uploader refinement */
div[data-testid="stFileUploader"] > div {{
    background: #1a1a1a;
    border-radius: 8px;
    border: 1px dashed #555;
    color: #fafafa;
}}

div[data-testid="stFileUploader"] button {{
    background: #fafafa;
    color: #0a0a0a;
    border: none;
    border-radius: 8px;
}}

/* Form element tweaks */
.stSelectbox, .stRadio {{
    color: #fafafa;
}}

select, .stSelectbox select, .stMultiselect select {{
    background: #1a1a1a;
    border: 1px solid #555;
    color: #fafafa;
    padding: 8px 10px;
    border-radius: 8px;
}}

/* Slider (range) styling */
input[type="range"] {{
    -webkit-appearance: none;
    height: 4px;
    background: #555;
    border-radius: 4px;
}}
input[type="range"]::-webkit-slider-thumb {{
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #fafafa;
    box-shadow: 0 0 8px rgba(250, 250, 250, 0.3);
    margin-top: -7px;
}}

/* Header/title styling */
.section h1 {{
    font-size: 2.8rem;
    font-weight: 700;
    margin: 0 0 4px 0;
    color: var(--text);
}}
.section p {{
    color: var(--muted);
    margin-top: 0;
    font-size: 1.1rem;
}}

.section {{
    background:var(--card);
    border: 1px solid #333;
    border-radius:12px;
    padding:1.6rem;
    margin-bottom:1.2rem;
    box-shadow: none;
}}

.section:hover {{
    transform: none;
    box-shadow: none;
    border-color: #777;
}}

.kpi {{
    background: transparent;
    border: 1px solid #333;
    border-radius:10px;
    padding:1.2rem;
}}

.kpi:hover {{
    transform: none;
    box-shadow: none;
    border-color: #777;
}}

.kpi-value {{
    font-size: 2.2rem;
    font-weight:600;
    color:var(--text);
}}

.health-glow {{
    border-color: #fafafa;
}}

.stButton>button {{
    background: #fafafa;
    color: #0a0a0a;
    border-radius:8px;
    padding:.65rem 1.1rem;
    font-weight:700;
    border:none;
}}

.stButton>button:hover {{
    transform: scale(1.02);
    box-shadow: none;
}}

.download-btn {{
    display:inline-block;
    background: #fafafa;
    color: #0a0a0a;
    padding:.6rem 1rem;
    border-radius:8px;
    text-decoration:none;
    font-weight:700;
}}

input, select, textarea {{
    transition: all .18s ease;
    border-radius:8px;
    border: 1px solid #555;
    background: #1a1a1a;
    color: #fafafa;
}}

input:focus, select:focus, textarea:focus {{
    box-shadow: none;
    border-color: #fafafa;
}}

/* Responsive tweaks for charts */
@media (max-width: 900px) {{
  .kpi-value {{ font-size:1.6rem; }}
  .section {{ padding:1.2rem; }}
}}
</style>
""", unsafe_allow_html=True)

# ================= SERVER-SIDE LOGIN (blocks app until signed in) =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = {}

if not st.session_state.logged_in:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown("""
        <div style='max-width:560px;margin:64px auto;padding:24px;background:#1a1a1a;border-radius:12px'>
        <h2 style='color:#fafafa;margin-top:0;'>Please sign in</h2>
        <p style='color:#a3a3a3;margin-top:0;margin-bottom:12px;'>Enter your email, password, and role to continue.</p>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            role = st.text_input("Role")
            submitted = st.form_submit_button("Log in")
            if submitted:
                st.session_state.user = {"email": email, "role": role}
                st.session_state.logged_in = True
                if hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
                else:
                    try:
                        set_query_params(_login=str(datetime.now().timestamp()))
                    except Exception:
                        pass

        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    st.markdown("<div style='color:#fafafa; font-size:14px; margin-bottom:12px'>Configure data & model parameters</div>", unsafe_allow_html=True)
    
    st.markdown("#### Data")
    data_mode = st.radio("Data Source", ["Upload CSV Dataset", "Simulated Data"], label_visibility="collapsed")
    
    st.markdown("#### Model")
    model_type = st.selectbox("Model", ["Linear Regression", "Random Forest", "LSTM", "Autoencoder"], label_visibility="collapsed")

    st.markdown("#### Prediction")
    prediction_horizon = st.slider(
        "Prediction Horizon",
        1, 50, 10,
        disabled=(model_type == "Autoencoder")
    )

    st.markdown("#### Health & Anomaly")
    health_threshold = st.slider("Health Threshold (%)", 50, 95, 75)
    anomaly_limit = st.slider("Anomaly Limit", 1, 50, 10)

    st.markdown("#### Download")
    report_format = st.selectbox("Download Format", ["CSV", "JSON", "Text"], label_visibility="collapsed")

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
<a class="download-btn" href="data:application/octet-stream;base64,{b64}" download="digital_twin_report.{report_format.lower()}">
⬇️ Download Report
</a>
""", unsafe_allow_html=True)

# ================= FOOTER =================
st.caption("Hybrid Digital Twin • Pop + Glow UI • Prediction Horizon • MCP Ready")
