# pages/stats.py

import random
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.i18n import t
from components.ui import metric_card, page_header
from data.constants import BUILDINGS_DATA, heatmap_data, hours, days_fr


def page_stats():
    st.markdown(
        page_header(t("stats_title"), "Analyse Statistique Descriptive — DIKW Niveaux Information & Knowledge"),
        unsafe_allow_html=True,
    )

    conso_vals = [b["conso"] for b in BUILDINGS_DATA]
    mean_val   = round(float(np.mean(conso_vals)), 1)
    std_val    = round(float(np.std(conso_vals)),  1)
    min_val    = int(min(conso_vals))
    max_val    = int(max(conso_vals))
    cv         = round(std_val / mean_val * 100, 1)

    # ── KPI row ───────────────────────────────────────────────
    cols = st.columns(5)
    kpis = [
        ("Moyenne",           f"{mean_val}", "kWh/jour",  "blue"),
        ("Écart-type",        f"{std_val}",  "kWh",       "teal"),
        ("Minimum",           f"{min_val}",  "kWh/jour",  "green"),
        ("Maximum",           f"{max_val}",  "kWh/jour",  "red"),
        ("Coeff. Variation",  f"{cv}%",      "dispersion","orange"),
    ]
    for col, (lbl, val, sub, clr) in zip(cols, kpis):
        with col:
            st.markdown(metric_card(lbl, val, sub, clr), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🌡️ Carte de Chaleur", "🔗 Corrélations"])

    # ── Distribution ─────────────────────────────────────────
    with tab1:
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown('<div class="content-card"><h3>Histogramme des Consommations</h3>', unsafe_allow_html=True)
            fig_h = go.Figure()
            fig_h.add_trace(go.Histogram(
                x=conso_vals, nbinsx=8,
                marker_color="#1E88E5", marker_line_color="#0A2463",
                marker_line_width=1.5, opacity=0.85,
            ))
            fig_h.add_vline(x=mean_val, line_dash="dash", line_color="#E53935",
                            annotation_text=f"Moy: {mean_val}", annotation_position="top right")
            fig_h.update_layout(
                height=280, margin=dict(l=0, r=0, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(245,250,255,1)",
                xaxis_title="kWh/jour", yaxis_title="Fréquence",
                font=dict(family="Space Grotesk", size=11),
            )
            st.plotly_chart(fig_h, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="content-card"><h3>Box Plot par Type</h3>', unsafe_allow_html=True)
            fig_bx  = go.Figure()
            types_u = list(set(b["type"] for b in BUILDINGS_DATA))
            pal     = ["#1E88E5", "#42A5F5", "#00B4D8", "#0D47A1", "#1565C0"]
            for i, btype in enumerate(types_u):
                vals     = [b["conso"] for b in BUILDINGS_DATA if b["type"] == btype]
                expanded = vals + [v * (0.85 + 0.3 * random.random()) for v in vals * 3]
                fig_bx.add_trace(go.Box(
                    y=expanded, name=btype[:15],
                    marker_color=pal[i % len(pal)],
                    boxpoints="all", jitter=0.3, pointpos=-1.6,
                ))
            fig_bx.update_layout(
                height=280, margin=dict(l=0, r=0, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(245,250,255,1)",
                yaxis_title="kWh/jour", showlegend=False,
                font=dict(family="Space Grotesk", size=11),
            )
            st.plotly_chart(fig_bx, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Full stats table
        st.markdown('<div class="content-card"><h3>Résumé Statistique Complet</h3>', unsafe_allow_html=True)
        stat_df = pd.DataFrame({
            "Indicateur": [
                "Moyenne (x̄)", "Médiane", "Variance (σ²)", "Écart-type (σ)",
                "Coeff. Variation", "Minimum", "Maximum", "Étendue", "Q1 (25%)", "Q3 (75%)",
            ],
            "Valeur": [
                f"{mean_val} kWh", f"{np.median(conso_vals):.1f} kWh",
                f"{np.var(conso_vals):.1f} kWh²", f"{std_val} kWh", f"{cv}%",
                f"{min_val} kWh", f"{max_val} kWh", f"{max_val - min_val} kWh",
                f"{np.percentile(conso_vals,25):.1f} kWh",
                f"{np.percentile(conso_vals,75):.1f} kWh",
            ],
            "Interprétation": [
                "Référence de comparaison", "Valeur centrale robuste", "Dispersion au carré",
                "Dispersion standard", "Hétérogène" if cv > 30 else "Homogène",
                "Bâtiment le moins énergivore", "Bâtiment le plus énergivore",
                "Plage totale", "Premier quartile", "Troisième quartile",
            ],
        })
        st.dataframe(stat_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Heatmap ───────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="content-card"><h3>🌡️ Carte de Chaleur Horaire</h3>', unsafe_allow_html=True)
        fig_ht = go.Figure(go.Heatmap(
            z=heatmap_data, x=[f"{h:02d}h" for h in hours], y=days_fr,
            colorscale="Blues", colorbar=dict(title="kWh"),
        ))
        fig_ht.update_layout(
            height=350, margin=dict(l=60, r=20, t=20, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Heure", yaxis_title="Jour",
            font=dict(family="Space Grotesk", size=11),
        )
        st.plotly_chart(fig_ht, use_container_width=True)
        st.markdown('<p style="font-size:0.78rem;color:#607D8B;">Zones bleu foncé = forte consommation (8h–18h)</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Correlations ─────────────────────────────────────────
    with tab3:
        st.markdown('<div class="content-card"><h3>🔗 Analyse de Corrélation</h3>', unsafe_allow_html=True)
        n = 50
        np.random.seed(42)
        temp      = np.random.uniform(15, 38, n)
        occup     = np.random.uniform(20, 95, n)
        conso_syn = 100 + 2.5 * temp + 1.8 * occup + np.random.normal(0, 20, n)

        fig_corr = go.Figure()
        fig_corr.add_trace(go.Scatter(
            x=temp, y=conso_syn, mode="markers", name="Temp vs Conso",
            marker=dict(color="#1E88E5", size=8, opacity=0.7),
        ))
        fig_corr.add_trace(go.Scatter(
            x=occup, y=conso_syn, mode="markers", name="Occupation vs Conso",
            marker=dict(color="#43A047", size=8, opacity=0.7),
        ))
        fig_corr.update_layout(
            height=300, margin=dict(l=0, r=0, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(245,250,255,1)",
            xaxis_title="Variable explicative", yaxis_title="Consommation (kWh)",
            font=dict(family="Space Grotesk", size=11), showlegend=True,
        )
        st.plotly_chart(fig_corr, use_container_width=True)

        r_temp = round(float(np.corrcoef(temp, conso_syn)[0, 1]), 3)
        r_occ  = round(float(np.corrcoef(occup, conso_syn)[0, 1]), 3)
        corr_df = pd.DataFrame({
            "Variable":       ["Température (°C)", "Taux d'Occupation (%)"],
            "Corrélation r":  [r_temp, r_occ],
            "R²":             [round(r_temp ** 2, 3), round(r_occ ** 2, 3)],
            "Interprétation": [
                "Forte corrélation positive" if abs(r_temp) > 0.7 else "Corrélation modérée",
                "Forte corrélation positive" if abs(r_occ)  > 0.7 else "Corrélation modérée",
            ],
        })
        st.dataframe(corr_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
