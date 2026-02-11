import streamlit as st

def render_sidebar():
    with st.sidebar:
        # ── User Section ─────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="
                padding: 1rem 0.8rem;
                border-radius: 10px;
                background: rgba(40, 45, 70, 0.4);
                margin-bottom: 1.2rem;
            ">
                <h4 style="margin: 0; color: #e0e7ff;">👤 Current User</h4>
                <div style="font-size: 1.15rem; font-weight: 600; color: #f1f5f9; margin: 0.4rem 0 0.1rem;">
                    {username}
                </div>
                <div style="color: #a5b4fc; font-size: 0.95rem;">
                    {role}
                </div>
            </div>
            """.format(
                username=st.session_state.user.get('username', '—'),
                role=st.session_state.user.get('role', '—')
            ),
            unsafe_allow_html=True
        )

        if st.button("🚪 Sign Out", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

        st.divider()

        # ── Controls Section ─────────────────────────────────────────────────
        st.markdown(
            '<h4 style="margin: 1.5rem 0 1rem; color: #e0e7ff;">⚙️ Dashboard Controls</h4>',
            unsafe_allow_html=True
        )

        # Data Source – Radio
        data_mode = st.radio(
            label="**Data Source**",
            options=["Upload CSV Dataset", "Simulated Data"],
            key="data_mode",
            horizontal=False,
            captions=["Upload your own CSV file", "Use generated example data"]
        )

        # Model – Selectbox
        model_type = st.selectbox(
            "**Prediction Model**",
            options=["Linear Regression", "Random Forest", "LSTM", "Autoencoder"],
            key="model_type"
        )

        # Sliders – with clearer labels
        prediction_horizon = st.slider(
            "**Prediction Horizon (steps)**",
            min_value=1,
            max_value=50,
            value=10,
            step=1,
            key="horizon",
            format="%d steps"
        )

        health_threshold = st.slider(
            "**Health Alert Threshold (%)**",
            min_value=50,
            max_value=95,
            value=75,
            step=5,
            key="health_threshold",
            format="%d%%"
        )

        anomaly_limit = st.slider(
            "**Max Allowed Anomalies**",
            min_value=1,
            max_value=50,
            value=10,
            step=1,
            key="anomaly_limit",
            format="%d"
        )

        # Report Format – Selectbox
        report_format = st.selectbox(
            "**Report Format**",
            options=["CSV", "JSON", "Text"],
            key="report_format"
        )

    return (
        data_mode,
        model_type,
        prediction_horizon,
        health_threshold,
        anomaly_limit,
        report_format
    )