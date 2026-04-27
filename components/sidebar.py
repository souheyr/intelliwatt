# components/sidebar.py
# Left navigation sidebar

import streamlit as st
from datetime import datetime
from utils.i18n import t
from data.constants import BUILDINGS_DATA


def render_sidebar():
    user     = st.session_state.current_user
    is_admin = user["role"] == "admin"

    with st.sidebar:
        # ── Logo ────────────────────────────────────────────
        st.markdown("""
        <div class="sidebar-logo">
            <div class="logo-icon">⚡</div>
            <div class="logo-title">IntelliWatt</div>
            <div class="logo-sub">Université Batna 2</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Language selector ────────────────────────────────
        lang_map = {"Français": "fr", "English": "en", "عربي": "ar"}
        cur_lang = next(k for k, v in lang_map.items() if v == st.session_state.lang)
        chosen   = st.selectbox(t("lang_label"), list(lang_map.keys()),
                                index=list(lang_map.keys()).index(cur_lang),
                                label_visibility="collapsed")
        if lang_map[chosen] != st.session_state.lang:
            st.session_state.lang = lang_map[chosen]
            st.rerun()

        # ── User card ────────────────────────────────────────
        b_label = "—"
        if user.get("building_assigned"):
            idx = (user["building_assigned"] or 1) - 1
            if 0 <= idx < len(BUILDINGS_DATA):
                b_label = BUILDINGS_DATA[idx]["nom"].split("—")[0].strip()

        st.markdown(f"""
        <div class="user-sidebar-card">
            <div class="u-name">{user.get('avatar','👤')} {user['full_name']}</div>
            <div class="u-role">{'🛡 Admin' if is_admin else '🔧 Tech'} · {b_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Nav helper ───────────────────────────────────────
        def nav_btn(page_key: str, label: str, icon: str):
            active = "✦ " if st.session_state.page == page_key else ""
            if st.button(f"{icon} {active}{label}", use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.page = page_key
                st.rerun()

        # ── Navigation groups ────────────────────────────────
        st.markdown('<div class="nav-section">Principal</div>', unsafe_allow_html=True)
        nav_btn("dashboard", t("nav_dashboard"), "📊")
        nav_btn("buildings", t("nav_buildings"), "🏢")
        nav_btn("optimize",  t("nav_optimize"),  "⚡")
        nav_btn("devices",   t("nav_devices"),   "🎛️")

        st.markdown('<div class="nav-section">Analyse</div>', unsafe_allow_html=True)
        nav_btn("scenarios", t("nav_scenarios"), "🧪")
        nav_btn("stats",     t("nav_stats"),     "📈")
        nav_btn("archive",   t("nav_archive"),   "💾")

        st.markdown('<div class="nav-section">Personnel</div>', unsafe_allow_html=True)
        nav_btn("profile",  t("nav_profile"),  "👤")
        nav_btn("settings", t("nav_settings"), "⚙️")
        nav_btn("help",     t("nav_help"),      "❓")

        if is_admin:
            st.markdown('<div class="nav-section">Administration</div>', unsafe_allow_html=True)
            nav_btn("admin", t("nav_admin"), "🛡")

        st.markdown("---")

        if st.button(f"🚪 {t('logout')}", use_container_width=True):
            st.session_state.logged_in    = False
            st.session_state.current_user = None
            st.session_state.page         = "dashboard"
            st.rerun()

        st.markdown(
            f'<div style="font-size:0.68rem;color:rgba(255,255,255,0.38);text-align:center;padding:8px 0 2px;">'
            f'IntelliWatt v3.0 | {datetime.now().strftime("%d/%m/%Y %H:%M")}'
            f'</div>',
            unsafe_allow_html=True,
        )
