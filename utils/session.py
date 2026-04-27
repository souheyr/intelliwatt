# utils/session.py
# Centralised session-state initialisation

import streamlit as st


def init_session():
    defaults = {
        "lang":          "fr",
        "page":          "dashboard",
        "logged_in":     False,
        "current_user":  None,
        "show_register": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
