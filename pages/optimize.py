# pages/optimize.py

import time
import random
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.i18n import t
from utils.database import save_opt_history, get_opt_history
from components.ui import alert_box, page_header
from data.constants import BUILDINGS_DATA


def page_optimize():
    user     = st.session_state.current_user
    is_admin = user["role"] == "admin"

    st.markdown(
        page_header(t("opt_title"), "Algorithme de Programmation Linéaire — Solveur CBC"),
        unsafe_allow_html=True,
    )

    if is_admin:
        building_names = [b["nom"] for b in BUILDINGS_DATA]
    else:
        b_id           = user.get("building_assigned", 1) or 1
        building_names = [b["nom"] for b in BUILDINGS_DATA if b["id"] == b_id]

    col_left, col_right = st.columns([1, 1.5])

    # ── Parameters panel ─────────────────────────────────────
    with col_left:
        st.markdown("<div class=\"content-card\"><h3>⚙️ Paramètres d'Optimisation</h3>", unsafe_allow_html=True)

        selected_b_name = st.selectbox("Bâtiment", building_names, key="opt_sel_bld")
        selected_b      = next(b for b in BUILDINGS_DATA if b["nom"] == selected_b_name)

        current_conso = st.number_input(
            "Consommation actuelle (kWh)",
            min_value=10, max_value=1000, value=selected_b["conso"],
        )

        period = st.radio(
            "Période tarifaire",
            ["Heures Pleines (HP) — Tarif élevé", "Heures Creuses (HC) — Tarif réduit"],
            key="opt_period_sel",
        )
        is_hp = "HP" in period

        tariff_color = "#E65100" if is_hp else "#2E7D32"
        tariff_bg    = "#FFF3E0" if is_hp else "#E8F5E9"
        tariff_msg   = "⚠ Heures Pleines — Coût: 18 DA/kWh" if is_hp else "✓ Heures Creuses — Coût: 11 DA/kWh"
        tariff_hint  = "Réduction forte recommandée (décaler charges)" if is_hp else "Optimisation standard — bonne période"

        st.markdown(f"""
        <div style="background:{tariff_bg};border-radius:8px;padding:12px;margin-top:8px;">
            <div style="font-weight:700;color:{tariff_color};font-size:0.85rem;">{tariff_msg}</div>
            <div style="font-size:0.78rem;color:#607D8B;margin-top:4px;">{tariff_hint}</div>
        </div>
        """, unsafe_allow_html=True)

        run_opt = st.button(f"🚀 {t('opt_btn')}", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Results panel ─────────────────────────────────────────
    with col_right:
        st.markdown('<div class="content-card"><h3>📊 Résultats</h3>', unsafe_allow_html=True)

        if run_opt:
            with st.spinner("Exécution de l'algorithme PL..."):
                time.sleep(0.5)

            base_saving_pct = random.uniform(8, 28) if is_hp else random.uniform(3, 18)
            if selected_b["statut"] == "Critique":
                base_saving_pct = max(base_saving_pct, 15)

            optimized    = round(current_conso * (1 - base_saving_pct / 100), 1)
            saving_kwh   = round(current_conso - optimized, 1)
            cost_per_kwh = 18 if is_hp else 11
            saving_cost  = round(saving_kwh * cost_per_kwh)

            # Cards
            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown(f"""<div class="opt-before">
                    <span class="val">{current_conso}</span>
                    <div class="lbl">kWh — {t('opt_before')}</div>
                </div>""", unsafe_allow_html=True)
            with r2:
                st.markdown(f"""<div class="opt-after">
                    <span class="val">{optimized}</span>
                    <div class="lbl">kWh — {t('opt_after')}</div>
                </div>""", unsafe_allow_html=True)
            with r3:
                st.markdown(f"""<div class="opt-saving">
                    <span class="val">-{round(base_saving_pct,1)}%</span>
                    <div class="lbl">{saving_kwh} kWh | {saving_cost} DA/j</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=optimized,
                delta={"reference": current_conso, "valueformat": ".0f", "suffix": " kWh"},
                gauge={
                    "axis": {"range": [0, selected_b["capacite"]], "ticksuffix": " kWh"},
                    "bar":  {"color": "#1E88E5"},
                    "steps": [
                        {"range": [0, selected_b["capacite"] * 0.75], "color": "#E8F5E9"},
                        {"range": [selected_b["capacite"] * 0.75, selected_b["capacite"] * 0.9], "color": "#FFF3E0"},
                        {"range": [selected_b["capacite"] * 0.9, selected_b["capacite"]], "color": "#FFEBEE"},
                    ],
                    "threshold": {"line": {"color": "#E53935", "width": 3}, "value": selected_b["capacite"] * 0.85},
                },
                title={"text": "Consommation Optimisée (kWh)", "font": {"size": 12}},
            ))
            fig_gauge.update_layout(
                height=220, margin=dict(l=20, r=20, t=40, b=10),
                paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Space Grotesk"),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Recommendations
            if is_hp:
                recs = [
                    ("success", f"Décaler {round(base_saving_pct*0.4,0):.0f}% de la charge vers les heures creuses (20h–8h)"),
                    ("info",    "Réduire l'éclairage de 20% dans les zones inoccupées"),
                    ("info",    "Programmer la mise en veille automatique des équipements"),
                ]
            else:
                recs = [
                    ("success",  "Optimisation HC activée — tarif réduit appliqué"),
                    ("info",     "Planifier maintenance et recharge en HC"),
                    ("warning",  "Vérifier les capteurs de présence dans les salles"),
                ]
            if selected_b["statut"] == "Critique":
                recs.insert(0, ("danger", f"URGENT: {selected_b['nom'].split('—')[0]} dépasse 85% de capacité"))

            for atype, msg in recs:
                st.markdown(alert_box(msg, atype), unsafe_allow_html=True)

            # Persist
            save_opt_history(user["id"], {
                "batiment":    selected_b_name.split("—")[0].strip(),
                "avant_kwh":   current_conso,
                "apres_kwh":   optimized,
                "economie_pct": round(base_saving_pct, 1),
                "economie_da": saving_cost,
                "periode":     "HP" if is_hp else "HC",
            })
            st.success(f"✅ Optimisation sauvegardée — Économie: {saving_kwh} kWh ({saving_cost} DA/jour)")

        else:
            st.markdown("""
            <div style="text-align:center;padding:50px 20px;color:#90A4AE;">
                <div style="font-size:3rem;opacity:0.35;margin-bottom:12px;">⚡</div>
                <div>Configurez les paramètres et lancez l'optimisation</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── History ───────────────────────────────────────────────
    history = get_opt_history(user["id"])
    if history:
        st.markdown('<div class="content-card"><h3>📋 Historique des Optimisations</h3>', unsafe_allow_html=True)
        hist_data = [{
            "Date":          row[8][:16] if row[8] else "",
            "Bâtiment":      row[2],
            "Avant (kWh)":   row[3],
            "Après (kWh)":   row[4],
            "Économie (%)":  f"-{row[5]}%",
            "Économie (DA)": f"{row[6]} DA",
            "Période":       row[7],
        } for row in history]
        st.dataframe(pd.DataFrame(hist_data), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
