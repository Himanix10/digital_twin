import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg: linear-gradient(to bottom, #2c3e50 0%, #1a202c 100%);
        --bg-card: rgba(30, 35, 55, 0.88);
        --border: rgba(100, 120, 255, 0.20);
        --text: #f1f5f9;
        --text-muted: #cbd5e1;
        --accent: #6366f1;
        --accent-dark: #4f46e5;
        --glow-color: rgba(168, 85, 247, 0.50);
        --metric-bright: #e0d7ff;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif !important;
        background: var(--bg) !important;
        color: var(--text) !important;
        background-attachment: fixed;
    }

    .stApp { background: transparent !important; }
    .stApp > header { display: none; }

    section[data-testid="stSidebar"] {
        background: rgba(20, 25, 40, 0.96) !important;
        backdrop-filter: blur(12px) !important;
        border-right: 1px solid var(--border) !important;
    }

    .main .block-container {
        padding: 2rem 2.5rem 4rem !important;
        max-width: 1440px !important;
    }

    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.6px;
        background: linear-gradient(90deg, #a855f7, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
    }

    /* Glassmorphic cards */
    .glass-card {
        background: var(--bg-card) !important;
        backdrop-filter: blur(14px) saturate(160%) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 1.8rem 2rem !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.32) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1.8rem;
    }

    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 40px rgba(0,0,0,0.38) !important;
    }

    /* Metric containers with hover pop effect */
    .metric-container {
        background: rgba(40, 45, 70, 0.70);
        border: 1px solid rgba(120,130,255,0.18);
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        text-align: center;
        transition: all 0.28s ease;
        min-height: 180px;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }

    .metric-container:hover {
        transform: scale(1.04);
        background: rgba(50, 55, 85, 0.90);
        border-color: var(--accent);
        box-shadow: 0 0 18px rgba(99,102,241,0.25);
    }

    /* Bright + soft glow for metric values */
    .metric-value-visible {
        font-weight: 800 !important;
        font-size: 2.95rem !important;
        color: var(--metric-bright) !important;
        text-shadow: 
            0 0 6px var(--glow-color),
            0 0 12px var(--glow-color);
        line-height: 1.05;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 1rem;
        color: #e2e8f0;
        font-weight: 500;
        margin-top: 0.6rem;
    }

    /* Status pills */
    .status-healthy   { background: rgba(34,197,94,0.25); color: #bbf7d0; border: 1px solid rgba(34,197,94,0.55); }
    .status-warning   { background: rgba(245,158,11,0.25); color: #fde68a; border: 1px solid rgba(245,158,11,0.55); }
    .status-critical  { background: rgba(239,68,68,0.25); color: #fca5a5; border: 1px solid rgba(239,68,68,0.55); }

    .status-pill {
        padding: 0.65rem 1.8rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 1.45rem;
        display: inline-block;
    }

    /* ──────────────────────────────────────────────────────────────── */
    /* SIDEBAR VISIBILITY FIX ────────────────────────────────────────── */
    /* ──────────────────────────────────────────────────────────────── */

    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #f1f5f9 !important;
    }

    /* Radio buttons */
    section[data-testid="stSidebar"] [role="radiogroup"] label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] input + div {
        border-color: #94a3b8 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] input:checked + div {
        background-color: var(--accent) !important;
        border-color: var(--accent) !important;
    }

    /* ── SELECTBOX / DROPDOWN ── strong visibility fix ── */
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Selected value in the box */
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select-display-value"] {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        background-color: rgba(40, 45, 70, 0.92) !important;
        border: 1px solid #7c8eff !important;
        border-radius: 8px !important;
    }

    /* Dropdown menu */
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] {
        background-color: #1e293b !important;
        border: 1px solid #6366f1 !important;
    }

    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="option"] {
        color: #e2e8f0 !important;
        background-color: #1e293b !important;
    }

    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="option"]:hover,
    section[data-testid="stSidebar"] .stSelectbox [aria-selected="true"] {
        background-color: #6366f1 !important;
        color: white !important;
    }

    /* Dropdown arrow */
    section[data-testid="stSidebar"] .stSelectbox svg {
        fill: #c7d2fe !important;
        opacity: 1 !important;
    }

    /* Sliders */
    section[data-testid="stSidebar"] [data-testid="stSlider"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSlider"] .stSliderValue,
    section[data-testid="stSidebar"] [data-testid="stThumbValue"] {
        color: #e0d7ff !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stThumbValue"] {
        background: #6366f1 !important;
    }

    section[data-testid="stSidebar"] .stSliderTrack {
        background: rgba(99,102,241,0.45) !important;
    }

    section[data-testid="stSidebar"] .stSliderRail {
        background: rgba(99,102,241,0.25) !important;
    }

    /* Sign Out button */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
        color: white !important;
        border: none !important;
    }

    /* General inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(30, 35, 55, 0.85) !important;
        border: 1px solid rgba(120,130,255,0.22) !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
    }

    hr {
        border-color: rgba(120,130,255,0.10);
        margin: 2.4rem 0;
    }

    /* ──────────────────────────────────────────────────────────────── */
    /* ── ONLY AUTH PAGE TEXT VISIBILITY FIX ────────────────────────── */
    /* ──────────────────────────────────────────────────────────────── */

    /* Auth page labels (Username, Password, etc.) */
    [data-testid="stAppViewContainer"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Auth page input placeholders & text */
    [data-testid="stAppViewContainer"] .stTextInput > div > div > input,
    [data-testid="stAppViewContainer"] .stTextInput > div > div > input::placeholder {
        color: #e2e8f0 !important;
        background-color: rgba(30, 35, 55, 0.95) !important;
        border: 1px solid #7c8eff !important;
        font-size: 1.05rem !important;
    }

    [data-testid="stAppViewContainer"] .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99,102,241,0.35) !important;
    }

    /* Auth page radio (Login/Register) */
    [data-testid="stAppViewContainer"] [role="radiogroup"] label {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stRadio"] input + div {
        border-color: #94a3b8 !important;
    }

    [data-testid="stAppViewContainer"] [data-testid="stRadio"] input:checked + div {
        background-color: #ef4444 !important;
        border-color: #ef4444 !important;
    }

    /* Password eye icon */
    [data-testid="stAppViewContainer"] .stTextInput button {
        color: #c7d2fe !important;
        background: transparent !important;
    }
    /* ================= AUTH RADIO FIX ================= */

/* Login / Register text visibility fix */
      [data-testid="stAppViewContainer"] [role="radiogroup"] label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
}

/* Unselected radio text */
[data-testid="stAppViewContainer"] [role="radiogroup"] span {
    color: #ffffff !important;
}

/* Selected radio background */
[data-testid="stAppViewContainer"] [data-testid="stRadio"] input:checked + div {
    background-color: #ef4444 !important;
    border-color: #ef4444 !important;
}

/* Radio circle */
[data-testid="stAppViewContainer"] [data-testid="stRadio"] input + div {
    border-color: #cbd5e1 !important;
}
                /* ================= AUTH RADIO FIX ================= */

/* Login / Register text visibility fix */
[data-testid="stAppViewContainer"] [role="radiogroup"] label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
}

/* Unselected radio text */
[data-testid="stAppViewContainer"] [role="radiogroup"] span {
    color: #ffffff !important;
}

/* Selected radio background */
[data-testid="stAppViewContainer"] [data-testid="stRadio"] input:checked + div {
    background-color: #ef4444 !important;
    border-color: #ef4444 !important;
}

/* Radio circle */
[data-testid="stAppViewContainer"] [data-testid="stRadio"] input + div {
    border-color: #cbd5e1 !important;
}



    </style>
    """, unsafe_allow_html=True)