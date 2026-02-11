import streamlit as st
import json
import os
from hashlib import sha256

USER_DB = "data/users.json"

def _load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USER_DB, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def _hash(password):
    return sha256(password.encode('utf-8')).hexdigest()

def render_auth():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    if st.session_state.logged_in:
        return True

    empty_left, main_col, empty_right = st.columns([1, 3, 1])

    with main_col:
        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <h1 style='
            text-align: center;
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -1.2px;
            margin-bottom: 0.5rem;
        '>
            Hybrid Digital Twin
        </h1>
        <p style='
            text-align: center;
            color: #a0aec0;
            font-size: 1.3rem;
            margin-bottom: 3rem;
        '>
            Predictive Intelligence Platform
        </p>
        """, unsafe_allow_html=True)

        mode = st.radio(
            label="",
            options=["Login", "Register"],
            horizontal=True,
            label_visibility="collapsed",
            key="auth_mode"
        )

        with st.form(key="auth_form", clear_on_submit=True):
            username = st.text_input(
                "Username",
                placeholder="your.name",
                key="username_input"
            )

            if mode == "Register":
                role = st.selectbox(
                    "Role",
                    ["Operator", "Engineer", "Supervisor", "Analyst", "Admin"],
                    key="role_select"
                )
            else:
                role = None

            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                key="password_input"
            )

            submit = st.form_submit_button(
                f" {mode} ",
                use_container_width=True,
                type="primary"
            )

        if submit:
            users = _load_users()

            if mode == "Register":
                if not username.strip() or not password.strip():
                    st.error("Please fill in all fields", icon="⚠️")
                elif username in users:
                    st.error("Username already exists", icon="🚫")
                else:
                    users[username] = {
                        "password": _hash(password),
                        "role": role
                    }
                    _save_users(users)
                    st.success("Account created! You can now log in.", icon="✅")

            else:  # Login
                if username not in users:
                    st.error("User not found", icon="🚫")
                elif users[username]["password"] != _hash(password):
                    st.error("Incorrect password", icon="🔒")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "username": username,
                        "role": users[username]["role"]
                    }
                    st.rerun()

    return False