import streamlit as st

# ── Import your modules ───────────────────────────────────────────────
from ui.auth import render_auth
from ui.dashboard import render_dashboard
from ui.styles import apply_styles

# ── Apply global styles as early as possible ──────────────────────────
apply_styles()

# ── Page configuration (should come very early) ───────────────────────
st.set_page_config(
    page_title="Hybrid Digital Twin",
    layout="wide",
    initial_sidebar_state="collapsed",   # or "expanded" depending on preference
    page_icon="🧬",                      # optional: nice touch
    menu_items={
        'Get Help': 'https://github.com/yourusername/digital-twin',  # optional
        'Report a bug': "mailto:your@email.com",
        'About': "Hybrid Digital Twin • Predictive Maintenance Dashboard\nv0.1"
    }
)

# ── Authentication gate ───────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

authenticated = render_auth()

if not authenticated:
    # No need to call st.stop() explicitly in most cases —
    # render_auth() already returns False and nothing else runs
    # But keeping it is fine for clarity
    st.stop()

# ── Main dashboard content ────────────────────────────────────────────
render_dashboard()