# pages/scenarios.py

import random
import streamlit as st
import pandas as pd
import numpy as np
from utils.i18n import t
from components.ui import metric_card, page_header
from data.constants import SCENARIOS


def page_scenarios():
    st.markdown(page_header(t("scen_title"), t("scen_desc")), unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Scénarios Détaillés", "📊 Tableau Récapitulatif"])

    # ── Detailed cards ────────────────────────────────────────
    with tab1:
        for scen in SCENARIOS:
            status_css = "pass" if scen["status"] == "PASS" else "fail"
            nom     = scen["nom_fr"]
            comment = scen["comment_fr"]

            with st.expander(f"[#{scen['id']}] {nom} — {scen['status']}", expanded=(scen["id"] == 1)):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"""
                    <div class="scenario-row {status_css}">
                        <div class="s-title">{nom}</div>
                        <div class="s-param">📌 {scen['params']}</div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px;">
                        <div style="background:#FFF3E0;border-radius:8px;padding:12px;">
                            <div style="font-size:0.70rem;color:#E65100;text-transform:uppercase;font-weight:700;margin-bottom:4px;">Résultat Obtenu</div>
                            <div style="font-size:0.84rem;color:#37474F;">{scen['obtained']}</div>
                        </div>
                        <div style="background:#E8F5E9;border-radius:8px;padding:12px;">
                            <div style="font-size:0.70rem;color:#2E7D32;text-transform:uppercase;font-weight:700;margin-bottom:4px;">Résultat Attendu</div>
                            <div style="font-size:0.84rem;color:#37474F;">{scen['expected']}</div>
                        </div>
                    </div>
                    <div style="margin-top:10px;background:#E3F2FD;border-radius:8px;padding:12px;">
                        <div style="font-size:0.70rem;color:#1565C0;text-transform:uppercase;font-weight:700;margin-bottom:4px;">Commentaire</div>
                        <div style="font-size:0.84rem;color:#37474F;">{comment}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    type_icons = {"critique": "⚠", "normal": "✓", "gaspillage": "!", "panne": "✕"}
                    t_icon     = type_icons.get(scen["type"], "•")
                    badge_cls  = "badge-pass" if scen["status"] == "PASS" else "badge-fail"
                    sav_color  = "#43A047" if scen["saving_pct"] > 0 else "#E53935"
                    sav_sign   = "−" if scen["saving_pct"] > 0 else ""

                    st.markdown(f"""
                    <div style="text-align:center;padding:16px 10px;">
                        <div style="font-size:2.5rem;margin-bottom:8px;">{t_icon}</div>
                        <div style="margin-bottom:10px;"><span class="badge {badge_cls}">{scen['status']}</span></div>
                        <div style="font-size:1.6rem;font-weight:800;color:{sav_color};">{sav_sign}{scen['saving_pct']}%</div>
                        <div style="font-size:0.73rem;color:#78909C;">Économie potentielle</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button("▶ Simuler", key=f"scen_run_{scen['id']}", use_container_width=True):
                        sim = round(scen["saving_pct"] * (0.9 + 0.2 * random.random()), 1)
                        st.success(f"Simulation: économie = {sim}%")

    # ── Summary table ─────────────────────────────────────────
    with tab2:
        st.markdown('<div class="content-card"><h3>Tableau Récapitulatif</h3>', unsafe_allow_html=True)
        recap = [
            {
                "#":            s["id"],
                "Scénario":     s["nom_fr"],
                "Type":         s["type"].capitalize(),
                "Obtenu":       s["obtained"][:50] + "...",
                "Attendu":      s["expected"][:50] + "...",
                "Économie (%)": s["saving_pct"],
                "Statut":       s["status"],
            }
            for s in SCENARIOS
        ]
        st.dataframe(pd.DataFrame(recap), use_container_width=True, hide_index=True)

        c1, c2, c3 = st.columns(3)
        pass_c = sum(1 for s in SCENARIOS if s["status"] == "PASS")
        fail_c = len(SCENARIOS) - pass_c
        avg_s  = round(float(np.mean([s["saving_pct"] for s in SCENARIOS if s["saving_pct"] > 0])), 1)

        with c1: st.markdown(metric_card("PASS",          str(pass_c), "scénarios validés", "green"),  unsafe_allow_html=True)
        with c2: st.markdown(metric_card("FAIL",          str(fail_c), "scénarios échoués", "red"),    unsafe_allow_html=True)
        with c3: st.markdown(metric_card("Économie Moy.", f"{avg_s}%", "sur scénarios PASS", "teal"), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
