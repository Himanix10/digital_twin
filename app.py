import streamlit as st

# ✅ MUST be the FIRST Streamlit command
st.set_page_config(
    page_title="Hybrid Digital Twin",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🧬",
    menu_items={
        'Get Help': 'https://github.com/yourusername/digital-twin',
        'Report a bug': "mailto:your@email.com",
        'About': "Hybrid Digital Twin • Predictive Maintenance Dashboard\nv0.1"
    }
)

# ── Now import modules ─────────────────────────────
from ui.styles import apply_styles
from ui.auth import render_auth
from ui.dashboard import render_dashboard

# ── Apply styles AFTER page config ─────────────────
apply_styles()

# ── Authentication Gate ───────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

authenticated = render_auth()

if not authenticated:
    st.stop()

# ── Main Dashboard ────────────────────────────────
render_dashboard()
