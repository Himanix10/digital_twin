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


# ================= SAFE RERUN =================
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.stop()


# ================= USER PERSISTENCE =================
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Hybrid Digital Twin",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= THEME =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {
  --bg1:#eaf0ff;
  --bg2:#f6f8fc;
  --card:#ffffff;
  --border:#d6def5;
  --text:#1f2937;
  --blue:#2563eb;
  --healthy:#16a34a;
  --warning:#f59e0b;
  --critical:#dc2626;
}

.stApp {
  background:linear-gradient(135deg,var(--bg1),var(--bg2));
  font-family:'Inter',sans-serif;
}

.section {
  background:var(--card);
  border:1px solid var(--border);
  border-radius:16px;
  padding:1.8rem;
  margin-bottom:1.4rem;
  box-shadow:0 12px 24px rgba(0,0,0,0.06);
}

.kpi {
  background:#f9fafb;
  border:1px solid var(--border);
  border-radius:14px;
  padding:1.4rem;
  cursor:pointer;
  transition:.2s;
}

.kpi:hover {
  transform:scale(1.03);
  border-color:var(--blue);
  box-shadow:0 0 0 2px rgba(37,99,235,.25),
             0 12px 22px rgba(37,99,235,.18);
}

.kpi-value {
  font-size:2.2rem;
  font-weight:700;
}

.health-glow-healthy { box-shadow:0 0 18px rgba(22,163,74,.35); }
.health-glow-warning { box-shadow:0 0 18px rgba(245,158,11,.35); }
.health-glow-critical { box-shadow:0 0 22px rgba(220,38,38,.45); }

.download-btn {
  background:linear-gradient(135deg,#3b82f6,#6366f1);
  color:white;
  padding:.7rem 1.2rem;
  border-radius:10px;
  font-weight:700;
  text-decoration:none;
}
</style>
""", unsafe_allow_html=True)


# ================= AUTH SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ================= LOGIN / REGISTER =================
if not st.session_state.logged_in:

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            st.subheader("Workspace Login")
            user = st.text_input("User")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                users_db = load_users()     # ✅ FIX: reload from disk
                u = users_db.get(user)

                if u and u["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    safe_rerun()
                else:
                    st.error("Invalid credentials")

    with tab_register:
        with st.form("register_form"):
            st.subheader("Register Workspace User")
            new_user = st.text_input("User")
            role = st.text_input("Role")
            new_password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register")

            if submit:
                users_db = load_users()
                if new_user in users_db:
                    st.error("User already exists")
                elif not new_user or not role or not new_password:
                    st.error("All fields required")
                else:
                    users_db[new_user] = {
                        "password": new_password,
                        "role": role
                    }
                    save_users(users_db)
                    st.success("Registered successfully. Please login.")

    st.stop()


# ================= SIDEBAR =================
with st.sidebar:
    st.markdown(f"### 👋 HI {st.session_state.current_user}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        safe_rerun()

    st.markdown("---")

    data_mode = st.radio("Data Source", ["Upload CSV Dataset", "Simulated Data"])
    model_type = st.selectbox("Model", ["Linear Regression", "Random Forest", "LSTM", "Autoencoder"])
    prediction_horizon = st.slider("Prediction Horizon", 1, 50, 10, disabled=(model_type == "Autoencoder"))
    health_threshold = st.slider("Health Threshold (%)", 50, 95, 75)
    anomaly_limit = st.slider("Anomaly Limit", 1, 50, 10)
    report_format = st.selectbox("Download Format", ["CSV", "JSON", "Text"])


# ================= HEADER =================
st.markdown("""
<div class="section">
<h1>Hybrid Digital Twin</h1>
<p>AI-Driven Predictive Monitoring • System Health & Anomaly Intelligence</p>
</div>
""", unsafe_allow_html=True)


# ================= DATA =================
if data_mode == "Upload CSV Dataset":
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
    else:
        st.stop()
else:
    df = pd.DataFrame({
        "temperature": 50 + np.random.randn(200),
        "vibration": 30 + np.random.randn(200),
        "pressure": 100 + np.random.randn(200)
    })

numeric_df = df.select_dtypes(include=np.number)


# ================= SENSOR SELECTION =================
st.markdown('<div class="section">', unsafe_allow_html=True)
sensors = st.multiselect("Sensors", numeric_df.columns, default=list(numeric_df.columns[:2]))
st.markdown('</div>', unsafe_allow_html=True)


# ================= DATA QUALITY =================
dq = compute_data_quality(numeric_df, sensors)

st.markdown('<div class="section">', unsafe_allow_html=True)
cols = st.columns(4)
labels = ["Missing %", "Noise", "Outliers", "Quality"]
values = [
    f"{dq['missing_pct']:.1f}%",
    f"{dq['noise']:.2e}",
    f"{dq['outlier_pct']:.1f}%",
    f"{dq['quality_score']:.1f}%"
]
for c, l, v in zip(cols, labels, values):
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
    status, glow, color = "Critical", "health-glow-critical", "var(--critical)"
elif health < health_threshold + 10:
    status, glow, color = "Warning", "health-glow-warning", "var(--warning)"
else:
    status, glow, color = "Healthy", "health-glow-healthy", "var(--healthy)"


# ================= KPIs =================
st.markdown('<div class="section">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='kpi {glow}'><div>Health</div><div class='kpi-value' style='color:{color}'>{health:.1f}%</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='kpi {glow}'><div>Status</div><div class='kpi-value' style='color:{color}'>{status}</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='kpi'><div>Anomalies</div><div class='kpi-value'>{len(anomalies)}</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ================= PLOT =================
st.markdown('<div class="section"><h3>System Behaviour, Prediction & Anomalies</h3>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(13,5))
ax.plot(actual, label="Actual")
ax.plot(predicted, "--", label="Predicted")

if len(future) > 0:
    ax.plot(range(len(actual), len(actual) + len(future)), future, ":", label="Future")

if len(anomalies) > 0:
    ax.scatter(anomalies, np.array(actual)[anomalies], color="red", label="Anomaly")

ax.legend()
ax.grid(alpha=.3)
st.pyplot(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ================= DOWNLOAD =================
report = {
    "user": st.session_state.current_user,
    "timestamp": datetime.now().isoformat(),
    "model": model_type,
    "health": health,
    "status": status,
    "anomalies": len(anomalies),
    "prediction_horizon": prediction_horizon
}

buf = BytesIO()
if report_format == "CSV":
    pd.DataFrame([report]).to_csv(buf, index=False)
elif report_format == "JSON":
    buf.write(json.dumps(report, indent=2).encode())
else:
    buf.write("\n".join(f"{k}: {v}" for k, v in report.items()).encode())

b64 = base64.b64encode(buf.getvalue()).decode()
st.markdown(
    f"<a class='download-btn' href='data:application/octet-stream;base64,{b64}' "
    f"download='digital_twin_report.{report_format.lower()}'>Download Report</a>",
    unsafe_allow_html=True
)

st.caption("Hybrid Digital Twin • Industrial AI • MCP Level System")
