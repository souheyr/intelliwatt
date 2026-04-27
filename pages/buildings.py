# pages/buildings.py

import streamlit as st
import plotly.graph_objects as go
from utils.i18n import t
from components.ui import alert_box, page_header, status_badge, load_pct, load_color, prog_bar
from data.constants import BUILDINGS_DATA, df_evolution


def page_buildings():
    user     = st.session_state.current_user
    is_admin = user["role"] == "admin"

    st.markdown(
        page_header(t("build_title"), "Vue complète et détaillée des bâtiments universitaires"),
        unsafe_allow_html=True,
    )

    if not is_admin:
        b_id = user.get("building_assigned", 1) or 1
        buildings_to_show = [b for b in BUILDINGS_DATA if b["id"] == b_id]
        st.markdown(
            alert_box("Accès limité — Vous ne pouvez consulter que votre bâtiment assigné.", "warning"),
            unsafe_allow_html=True,
        )
    else:
        buildings_to_show = BUILDINGS_DATA

    building_names = [b["nom"] for b in buildings_to_show]
    selected_name  = st.selectbox(t("build_select"), building_names)
    selected_b     = next(b for b in buildings_to_show if b["nom"] == selected_name)

    col1, col2 = st.columns([1, 2])

    with col1:
        pct     = load_pct(selected_b["conso"], selected_b["capacite"])
        col_pct = load_color(pct)
        st.markdown(f"""
        <div class="content-card">
            <h3>{t('build_details')}</h3>
            <table style="width:100%;font-size:0.88rem;border-collapse:collapse;">
                <tr><td style="padding:7px 0;color:#607D8B;font-weight:600;">🏢 Nom</td><td style="padding:7px 0;">{selected_b['nom']}</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;font-weight:600;">🏷 Type</td><td style="padding:7px 0;">{selected_b['type']}</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;font-weight:600;">⚡ Consommation</td><td style="padding:7px 0;font-weight:700;color:{col_pct};">{selected_b['conso']} kWh/j</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;font-weight:600;">📊 Capacité Max</td><td style="padding:7px 0;">{selected_b['capacite']} kWh</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;font-weight:600;">🏗 Étages</td><td style="padding:7px 0;">{selected_b['etage']}</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;font-weight:600;">📐 Surface</td><td style="padding:7px 0;">{selected_b['surface']:,} m²</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;font-weight:600;">🔰 Statut</td><td style="padding:7px 0;">{status_badge(selected_b['statut'])}</td></tr>
            </table>
            <div style="margin-top:12px;">
                <div style="font-size:0.78rem;color:#607D8B;margin-bottom:4px;">Taux de charge</div>
                {prog_bar(pct, col_pct)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        short = selected_name.split("—")[0].strip()
        b_data = df_evolution[[short]] if short in df_evolution.columns else df_evolution.iloc[:, :1]

        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(
            x=b_data.index, y=b_data.iloc[:, 0],
            mode="lines+markers",
            line=dict(color="#1E88E5", width=2.5),
            fill="tozeroy", fillcolor="rgba(30,136,229,0.08)",
            marker=dict(size=5),
        ))
        fig_b.add_hline(
            y=selected_b["capacite"], line_dash="dash",
            line_color="#E53935", annotation_text="Capacité Max",
        )
        fig_b.update_layout(
            height=280, margin=dict(l=0, r=0, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(245,250,255,1)",
            title="Évolution 30 jours", title_font_size=13,
            font=dict(family="Space Grotesk", size=11),
            yaxis_title="kWh/jour",
        )
        st.plotly_chart(fig_b, use_container_width=True)

    # ── Full table (admin only) ───────────────────────────────
    if is_admin:
        st.markdown('<div class="content-card"><h3>Tableau Complet des Bâtiments</h3>', unsafe_allow_html=True)
        rows_html = ""
        for b in BUILDINGS_DATA:
            pct_b = load_pct(b["conso"], b["capacite"])
            col_b = load_color(pct_b)
            rows_html += f"""
            <tr style="border-bottom:1px solid #E3F2FD;">
                <td style="padding:10px 8px;font-weight:600;">{b['nom']}</td>
                <td style="padding:10px 8px;color:#607D8B;">{b['type']}</td>
                <td style="padding:10px 8px;font-weight:700;color:{col_b};">{b['conso']} kWh</td>
                <td style="padding:10px 8px;">{b['capacite']} kWh</td>
                <td style="padding:10px 8px;">
                    <div style="background:#E3F2FD;border-radius:4px;height:6px;width:80px;display:inline-block;vertical-align:middle;margin-right:6px;overflow:hidden;">
                        <div style="width:{min(pct_b,100)}%;height:100%;background:{col_b};border-radius:4px;"></div>
                    </div>
                    <span style="font-size:0.80rem;color:{col_b};">{pct_b}%</span>
                </td>
                <td style="padding:10px 8px;">{status_badge(b['statut'])}</td>
            </tr>"""

        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;font-size:0.87rem;">
            <thead>
                <tr style="background:#0A2463;color:white;">
                    <th style="padding:10px 8px;text-align:left;">Bâtiment</th>
                    <th style="padding:10px 8px;text-align:left;">Type</th>
                    <th style="padding:10px 8px;text-align:left;">Consommation</th>
                    <th style="padding:10px 8px;text-align:left;">Capacité Max</th>
                    <th style="padding:10px 8px;text-align:left;">Charge</th>
                    <th style="padding:10px 8px;text-align:left;">Statut</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
