# pages/dashboard.py

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from utils.i18n import t
from components.ui import metric_card, alert_box, page_header
from data.constants import BUILDINGS_DATA, df_evolution


def page_dashboard():
    user          = st.session_state.current_user
    total_conso   = sum(b["conso"] for b in BUILDINGS_DATA)
    critical_count = sum(1 for b in BUILDINGS_DATA if b["statut"] == "Critique")
    active_count  = sum(1 for b in BUILDINGS_DATA if b["statut"] == "Actif")
    saving_pct    = 11.1
    potential_saving = round(total_conso * saving_pct / 100)

    st.markdown(page_header(
        t("nav_dashboard"),
        f"Université Batna 2 — {datetime.now().strftime('%A %d %B %Y')}",
        f"Connecté: {user['avatar']} {user['full_name']} | "
        f"{'🛡 Admin' if user['role']=='admin' else '🔧 Technicien'}",
    ), unsafe_allow_html=True)

    if critical_count > 0:
        st.markdown(
            alert_box(f"⚡ {critical_count} bâtiment(s) en état CRITIQUE — Intervention recommandée immédiatement", "danger"),
            unsafe_allow_html=True,
        )

    # ── KPIs ─────────────────────────────────────────────────
    cols = st.columns(4)
    with cols[0]: st.markdown(metric_card(t("dash_total_conso"), f"{total_conso:,}", t("kwh_day"), "blue"), unsafe_allow_html=True)
    with cols[1]: st.markdown(metric_card(t("dash_critical"), str(critical_count), "nécessitent attention", "red"), unsafe_allow_html=True)
    with cols[2]: st.markdown(metric_card(t("dash_savings"), f"{potential_saving:,}", f"kWh/jour (-{saving_pct}%)", "green"), unsafe_allow_html=True)
    with cols[3]: st.markdown(metric_card(t("dash_active"), str(active_count), "sur 8 bâtiments", "teal"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bar + Pie ─────────────────────────────────────────────
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="content-card"><h3>' + t("dash_by_building") + '</h3>', unsafe_allow_html=True)
        bar_colors  = ["#E53935" if b["statut"] == "Critique" else "#1E88E5" if b["statut"] == "Actif" else "#FB8C00" for b in BUILDINGS_DATA]
        short_names = [b["nom"].split("—")[0].strip() for b in BUILDINGS_DATA]

        fig = go.Figure(go.Bar(
            x=short_names, y=[b["conso"] for b in BUILDINGS_DATA],
            marker_color=bar_colors,
            text=[f"{b['conso']} kWh" for b in BUILDINGS_DATA],
            textposition="outside", marker_line_width=0,
        ))
        fig.add_scatter(
            x=short_names, y=[b["capacite"] for b in BUILDINGS_DATA],
            mode="markers+lines", name="Capacité Max",
            marker=dict(size=8, color="rgba(10,36,99,0.6)", symbol="diamond"),
            line=dict(color="rgba(10,36,99,0.3)", dash="dot"),
        )
        fig.update_layout(
            height=290, margin=dict(l=0, r=0, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(245,250,255,1)",
            showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1),
            font=dict(family="Space Grotesk", size=11), yaxis_title="kWh/jour",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="content-card"><h3>' + t("dash_by_type") + "</h3>", unsafe_allow_html=True)
        type_conso: dict[str, int] = {}
        for b in BUILDINGS_DATA:
            type_conso[b["type"]] = type_conso.get(b["type"], 0) + b["conso"]

        fig_pie = go.Figure(go.Pie(
            labels=list(type_conso.keys()), values=list(type_conso.values()),
            hole=0.55,
            marker=dict(colors=["#1E88E5", "#00B4D8", "#43A047", "#FB8C00", "#8E24AA"]),
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>%{value} kWh<extra></extra>",
        ))
        fig_pie.add_annotation(
            text=f"<b>{total_conso}</b><br>kWh/j", x=0.5, y=0.5,
            font=dict(size=14, color="#0A2463"), showarrow=False,
        )
        fig_pie.update_layout(
            height=290, margin=dict(l=10, r=10, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Space Grotesk", size=11),
            showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Evolution ─────────────────────────────────────────────
    st.markdown('<div class="content-card"><h3>' + t("dash_evolution") + "</h3>", unsafe_allow_html=True)
    palette = ["#1E88E5", "#E53935", "#43A047", "#FB8C00", "#8E24AA", "#00BCD4", "#FF5722", "#607D8B"]
    fig_ev  = go.Figure()
    for i, col_name in enumerate(df_evolution.columns):
        fig_ev.add_trace(go.Scatter(
            x=df_evolution.index, y=df_evolution[col_name],
            name=col_name, mode="lines",
            line=dict(color=palette[i % len(palette)], width=2),
            fill="tonexty" if i == 0 else None,
            fillcolor="rgba(30,136,229,0.05)",
        ))
    fig_ev.update_layout(
        height=280, margin=dict(l=0, r=0, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(245,250,255,1)",
        font=dict(family="Space Grotesk", size=11),
        legend=dict(orientation="h", yanchor="bottom", y=1),
        yaxis_title="kWh",
    )
    st.plotly_chart(fig_ev, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
