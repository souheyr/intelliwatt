# ============================================================
# PAGE: SETTINGS
# ============================================================

import streamlit as st

# ⚠️ IMPORTS nécessaires
from utils.i18n import t
from utils.database import update_preferences
from components.ui import page_header, metric_card


def page_settings():

    # ─────────────────────────────
    # sécurité session
    # ─────────────────────────────
    if "current_user" not in st.session_state:
        st.error("⛔ Utilisateur non connecté")
        return

    user = st.session_state.current_user

    # ─────────────────────────────
    # HEADER
    # ─────────────────────────────
    st.markdown(
        page_header(
            t("settings_title"),
            "Personnalisez l'interface, la langue et les préférences"
        ),
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ─────────────────────────────
    # COLONNE 1
    # ─────────────────────────────
    with col1:

        st.markdown(
            '<div class="setting-group"><h4>🌐 Langue et Région</h4>',
            unsafe_allow_html=True
        )

        lang_opts = {"Français": "fr", "English": "en", "العربية": "ar"}

        cur_lang = st.session_state.get("lang", "fr")

        cur_lang_label = next(
            k for k, v in lang_opts.items() if v == cur_lang
        )

        new_lang_label = st.selectbox(
            t("settings_lang"),
            list(lang_opts.keys()),
            index=list(lang_opts.keys()).index(cur_lang_label)
        )

        new_lang = lang_opts[new_lang_label]

        if new_lang != cur_lang:
            st.session_state.lang = new_lang
            st.session_state.current_user["language"] = new_lang

            update_preferences(
                user["id"],
                user.get("theme", "light"),
                new_lang,
                user.get("notifications", 1)
            )

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # ─────────────────────────────
        st.markdown(
            '<div class="setting-group"><h4>🔔 Notifications</h4>',
            unsafe_allow_html=True
        )

        notif_opts = {"Activées": 1, "Désactivées": 0}

        cur_notif = user.get("notifications", 1)
        notif_label = "Activées" if cur_notif else "Désactivées"

        new_notif_label = st.selectbox(
            "Notifications d'alerte",
            list(notif_opts.keys()),
            index=list(notif_opts.keys()).index(notif_label)
        )

        alert_critical = st.checkbox("Alertes bâtiments critiques", value=True)
        alert_optim = st.checkbox("Notifications d'optimisation", value=True)
        alert_archive = st.checkbox("Confirmations d'archivage", value=False)

        if st.button("💾 Sauvegarder Notifications", use_container_width=True):

            new_notif = notif_opts[new_notif_label]

            st.session_state.current_user["notifications"] = new_notif

            update_preferences(
                user["id"],
                user.get("theme", "light"),
                st.session_state.lang,
                new_notif
            )

            st.success("✅ Notifications sauvegardées")

        st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────
    # COLONNE 2
    # ─────────────────────────────
    with col2:

        st.markdown(
            '<div class="setting-group"><h4>🎨 Apparence</h4>',
            unsafe_allow_html=True
        )

        theme_opts = {"☀️ Clair": "light", "🌙 Sombre": "dark"}

        cur_theme = user.get("theme", "light")

        cur_theme_label = next(
            k for k, v in theme_opts.items() if v == cur_theme
        )

        new_theme_label = st.selectbox(
            t("settings_theme"),
            list(theme_opts.keys()),
            index=list(theme_opts.keys()).index(cur_theme_label)
        )

        new_theme = theme_opts[new_theme_label]

        if new_theme != cur_theme:
            st.session_state.current_user["theme"] = new_theme

            update_preferences(
                user["id"],
                new_theme,
                st.session_state.lang,
                user.get("notifications", 1)
            )

            st.info("Thème mis à jour")

        st.markdown('</div>', unsafe_allow_html=True)

        # ─────────────────────────────
        st.markdown(
            '<div class="setting-group"><h4>📊 Affichage</h4>',
            unsafe_allow_html=True
        )

        st.selectbox(
            "Actualisation auto",
            ["Désactivée", "5 min", "15 min", "30 min"]
        )

        st.selectbox(
            "Séparateur décimal",
            ["Virgule (,)", "Point (.)"]
        )

        st.selectbox(
            "Format date",
            ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"]
        )

        st.button("💾 Sauvegarder affichage")

        st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────
    # SYSTEM INFO
    # ─────────────────────────────
    st.markdown(
        '<div class="content-card"><h3>🖥️ Système</h3>',
        unsafe_allow_html=True
    )

    cols = st.columns(3)

    with cols[0]:
        st.markdown(metric_card("Version", "1.0", "IntelliWatt", "blue"), unsafe_allow_html=True)

    with cols[1]:
        st.markdown(metric_card("Mode", "Production", "Stable", "green"), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
