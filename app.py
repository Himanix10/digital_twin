import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '0'

# Limit TensorFlow to minimum memory
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'

import streamlit as st
import traceback

st.set_page_config(
    page_title="Hybrid Digital Twin",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🧬",
    menu_items={
        'Get Help': 'https://github.com/Himanix10/digital-twin',
        'Report a bug': "mailto:himanix10@email.com",
        'About': "Hybrid Digital Twin • Predictive Maintenance Dashboard\nv0.1"
    }
)

try:
    from ui.styles import apply_styles
    from ui.auth import render_auth
    from ui.dashboard import render_dashboard
except Exception as e:
    st.error(f"IMPORT ERROR: {e}")
    st.code(traceback.format_exc())
    st.stop()

apply_styles()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

authenticated = render_auth()

if not authenticated:
    st.stop()

try:
    render_dashboard()
except Exception as e:
    st.error(f"DASHBOARD CRASH: {e}")
    st.code(traceback.format_exc())