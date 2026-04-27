# ============================================================
# PAGE: HELP
# ============================================================

import streamlit as st

# ⚠️ IMPORTS MANQUANTS
from utils.i18n import t
from components.ui import page_header


def page_help():

    st.markdown(
        page_header(
            t("help_title"),
            "Documentation et guide d'utilisation IntelliWatt v3.0"
        ),
        unsafe_allow_html=True
    )

    tab_admin, tab_tech = st.tabs(
        ["🛡 Guide Administrateur", "🔧 Guide Technicien"]
    )

    # ─────────────────────────────
    # ADMIN ITEMS
    # ─────────────────────────────
    items_admin = [
        ("📊 Tableau de Bord", "Surveillez la consommation globale de tous les bâtiments. Les alertes colorées signalent les situations critiques."),
        ("🏢 Gestion des Bâtiments", "Consultez la liste complète. Cliquez pour voir les détails."),
        ("⚡ Optimisation", "Lancez l’optimisation énergétique globale du système."),
        ("🎛️ Contrôle Appareils", "Contrôle des équipements par bâtiment ou global."),
        ("💾 Archivage", "Export CSV et génération de rapports PDF."),
        ("🛡 Administration", "Gestion des utilisateurs et permissions."),
    ]

    with tab_admin:
        for title, desc in items_admin:
            st.markdown(f"""
            <div style="
                background:white;
                border-radius:12px;
                padding:16px;
                margin-bottom:10px;
                box-shadow:0 2px 10px rgba(10,36,99,0.08);
                border-left:4px solid #1E88E5;">
                <div style="font-weight:700;color:#0A2463;margin-bottom:5px;">
                    {title}
                </div>
                <div style="font-size:0.86rem;color:#455A64;line-height:1.6;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─────────────────────────────
    # TECH ITEMS
    # ─────────────────────────────
    items_tech = [
        ("🔒 Accès Limité", "Accès uniquement au bâtiment assigné."),
        ("🎛️ Contrôle Appareils", "Gestion des équipements locaux."),
        ("⚡ Optimisation", "Optimisation énergétique de votre zone."),
        ("⚠ Alertes", "Surveillance des anomalies."),
        ("💾 Export", "Export des données CSV."),
    ]

    with tab_tech:
        for title, desc in items_tech:
            st.markdown(f"""
            <div style="
                background:white;
                border-radius:12px;
                padding:16px;
                margin-bottom:10px;
                box-shadow:0 2px 10px rgba(10,36,99,0.08);
                border-left:4px solid #42A5F5;">
                <div style="font-weight:700;color:#0A2463;margin-bottom:5px;">
                    {title}
                </div>
                <div style="font-size:0.86rem;color:#455A64;line-height:1.6;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)
