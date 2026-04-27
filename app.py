# ============================================================
# IntelliWatt — Gestion Énergétique Universitaire
# Entry Point: app.py
# ============================================================

import streamlit as st

# ── Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="IntelliWatt — Université Batna 2",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Imports internes ──────────────────────────────────────
from utils.database import init_db
from utils.session import init_session
from utils.styles import inject_css
from utils.i18n import sync_language

from components.sidebar import render_sidebar

from pages.login import page_login
from pages.dashboard import page_dashboard
from pages.buildings import page_buildings
from pages.optimize import page_optimize
from pages.devices import page_devices
from pages.scenarios import page_scenarios
from pages.stats import page_stats
from pages.archive import page_archive
from pages.profile import page_profile
from pages.settings import page_settings
from pages.admin import page_admin
from pages.help import page_help


# ── Bootstrap ─────────────────────────────────────────────
init_db()
init_session()
inject_css()
sync_language()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "show_register" not in st.session_state:
    st.session_state.show_register = False
# ── Navigation Top (optionnel) ────────────────────────────
def top_nav():
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    pages = [
        ("dashboard", "📊 Dashboard"),
        ("buildings", "🏢 Buildings"),
        ("optimize", "⚡ Optimize"),
        ("devices", "🎛️ Devices"),
        ("scenarios", "🧪 Scenarios"),
        ("stats", "📈 Stats"),
        ("archive", "💾 Archive"),
        ("profile", "👤 Profile"),
        ("settings", "⚙️ Settings"),
        ("help", "❓ Help"),
    ]

    cols = st.columns(len(pages))

    for i, (key, label) in enumerate(pages):
        with cols[i]:
            if st.button(label, key=f"top_{key}"):
                st.session_state.page = key
                st.rerun()


def router():
    if not st.session_state.get("logged_in", False):
        page_login()
        return

    render_sidebar()
    top_nav()

    page = st.session_state.get("page", "dashboard")

    if page == "dashboard":
        page_dashboard()
    elif page == "buildings":
        page_buildings()
    elif page == "optimize":
        page_optimize()
    elif page == "devices":
        page_devices()
    elif page == "scenarios":
        page_scenarios()
    elif page == "stats":
        page_stats()
    elif page == "archive":
        page_archive()
    elif page == "profile":
        page_profile()
    elif page == "settings":
        page_settings()
    elif page == "help":
        page_help()
    else:
        page_dashboard()

