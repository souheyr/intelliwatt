# pages/archive.py

import io
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.i18n import t
from utils.database import save_archive, get_archive_log
from components.ui import page_header
from data.constants import BUILDINGS_DATA


def _load_pct(conso, capacite):
    return round((conso / capacite) * 100, 1)


def _generate_pdf(buildings_data, user_name: str):
    """Generate PDF via reportlab. Returns BytesIO buffer or None."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
        )
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=2 * cm, rightMargin=2 * cm,
                                topMargin=2 * cm, bottomMargin=2 * cm)
        styles   = getSampleStyleSheet()
        title_st = ParagraphStyle("T", parent=styles["Title"], fontSize=22,
                                  fontName="Helvetica-Bold",
                                  textColor=colors.HexColor("#0A2463"),
                                  spaceAfter=4, alignment=TA_CENTER)
        sub_st   = ParagraphStyle("S", parent=styles["Normal"], fontSize=11,
                                  textColor=colors.HexColor("#1E88E5"),
                                  spaceAfter=12, alignment=TA_CENTER)
        h2_st    = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14,
                                  fontName="Helvetica-Bold",
                                  textColor=colors.HexColor("#0A2463"),
                                  spaceBefore=16, spaceAfter=8)
        body_st  = ParagraphStyle("B", parent=styles["Normal"], fontSize=10,
                                  textColor=colors.HexColor("#37474F"),
                                  leading=14, spaceAfter=6)
        small_st = ParagraphStyle("Sm", parent=styles["Normal"], fontSize=8,
                                  textColor=colors.grey, alignment=TA_RIGHT)

        story = [
            Spacer(1, 0.3 * cm),
            Paragraph("⚡ IntelliWatt", title_st),
            Paragraph("Rapport Énergétique — Université Batna 2", sub_st),
            Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} | Par: {user_name}", small_st),
            HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1E88E5"), spaceAfter=12),
        ]

        total_conso = sum(b["conso"] for b in buildings_data)
        critical    = sum(1 for b in buildings_data if b["statut"] == "Critique")
        active      = sum(1 for b in buildings_data if b["statut"] == "Actif")
        potential   = round(total_conso * 0.111)

        story.append(Paragraph("Résumé Exécutif", h2_st))
        summary = [
            ["Indicateur", "Valeur", "Statut"],
            ["Consommation totale", f"{total_conso:,} kWh/jour", "—"],
            ["Bâtiments actifs", f"{active} / {len(buildings_data)}", "✓ Normal"],
            ["Bâtiments critiques", f"{critical}", "⚠ Attention" if critical > 0 else "✓ Aucun"],
            ["Économie potentielle", f"{potential} kWh/jour (-11.1%)", "→ Optimisation"],
            ["Économie financière", f"~{potential * 15:,} DA/mois", "→ Potentiel"],
        ]
        t_obj = Table(summary, colWidths=[7 * cm, 6 * cm, 5 * cm])
        t_obj.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0A2463")),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0), 10),
            ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F0F7FF"), colors.white]),
            ("GRID",       (0, 0), (-1, -1), 0.5, colors.HexColor("#BBDEFB")),
            ("FONTNAME",   (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",   (0, 1), (-1, -1), 9),
            ("ROWHEIGHT",  (0, 0), (-1, -1), 0.7 * cm),
        ]))
        story += [t_obj, Spacer(1, 0.5 * cm)]

        story.append(Paragraph("État des Bâtiments", h2_st))
        story.append(Paragraph(
            "Consommation énergétique actuelle par bâtiment avec taux de charge et statut opérationnel.",
            body_st,
        ))

        bld_rows = [["Bâtiment", "Type", "Conso (kWh)", "Capacité (kWh)", "Charge %", "Statut"]]
        for b in buildings_data:
            pct       = round(b["conso"] / b["capacite"] * 100, 1)
            status_str = "🔴 Critique" if b["statut"] == "Critique" else ("🟡 Maint." if b["statut"] == "Maintenance" else "🟢 Actif")
            bld_rows.append([
                b["nom"].split("—")[0].strip(),
                b["type"][:18],
                str(b["conso"]),
                str(b["capacite"]),
                f"{pct}%",
                status_str,
            ])
        bld_rows.append(["TOTAL", "—", str(total_conso), "—", "—", f"{active} actifs"])

        bld_t = Table(bld_rows, colWidths=[4.5 * cm, 4 * cm, 2.8 * cm, 2.8 * cm, 2 * cm, 2.5 * cm])
        bld_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0A2463")),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0), 9),
            ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.HexColor("#F0F7FF"), colors.white]),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E3F2FD")),
            ("FONTNAME",   (0, -1), (-1, -1), "Helvetica-Bold"),
            ("GRID",       (0, 0), (-1, -1), 0.5, colors.HexColor("#BBDEFB")),
            ("FONTNAME",   (0, 1), (-1, -2), "Helvetica"),
            ("FONTSIZE",   (0, 1), (-1, -1), 8),
            ("ROWHEIGHT",  (0, 0), (-1, -1), 0.65 * cm),
        ]))
        story.append(bld_t)

        doc.build(story)
        buf.seek(0)
        return buf.getvalue()
    except ImportError:
        return None


def page_archive():
    user = st.session_state.current_user

    st.markdown(
        page_header(t("arch_title"), "Sauvegarde, Export CSV & Génération de Rapports PDF Optimisés"),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    # ── Save snapshot ─────────────────────────────────────────
    with col1:
        st.markdown('<div class="content-card"><h3>💾 Enregistrement des Données</h3>', unsafe_allow_html=True)
        archive_building = st.selectbox(
            "Bâtiment à archiver",
            ["Tous les bâtiments"] + [b["nom"] for b in BUILDINGS_DATA],
        )
        archive_note = st.text_area("Note / Commentaire (optionnel)", height=80)

        if st.button(f"💾 {t('arch_save')}", use_container_width=True):
            if archive_building == "Tous les bâtiments":
                data     = {"buildings": BUILDINGS_DATA, "timestamp": datetime.now().isoformat(), "note": archive_note}
                bld_name = "Tous"
            else:
                b        = next(b for b in BUILDINGS_DATA if b["nom"] == archive_building)
                data     = {"building": b, "timestamp": datetime.now().isoformat(), "note": archive_note}
                bld_name = archive_building.split("—")[0].strip()

            save_archive(user["id"], user["username"], "snapshot", bld_name, data)
            st.success(f"✅ Données enregistrées — {datetime.now().strftime('%H:%M:%S')}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Export ───────────────────────────────────────────────
    with col2:
        st.markdown('<div class="content-card"><h3>📤 Export & Rapport PDF</h3>', unsafe_allow_html=True)

        if st.button(f"📊 {t('arch_export_csv')}", use_container_width=True):
            df_exp = pd.DataFrame(BUILDINGS_DATA)
            df_exp["charge_pct"]  = df_exp.apply(lambda r: _load_pct(r["conso"], r["capacite"]), axis=1)
            df_exp["export_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            csv_buf = io.StringIO()
            df_exp.to_csv(csv_buf, index=False, encoding="utf-8-sig")
            st.download_button(
                label="⬇ Télécharger le CSV",
                data=csv_buf.getvalue(),
                file_name=f"intelliwatt_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#E3F2FD;border-radius:8px;padding:12px;margin-bottom:12px;">
            <div style="font-weight:700;color:#1565C0;font-size:0.88rem;">📄 Rapport PDF Académique</div>
            <div style="font-size:0.78rem;color:#455A64;margin-top:4px;">
                Inclut: Résumé exécutif · Tableau des bâtiments · Recommandations
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"📑 {t('arch_export_pdf')}", use_container_width=True):
            with st.spinner("Génération du rapport PDF..."):
                pdf_bytes = _generate_pdf(BUILDINGS_DATA, user["full_name"])

            if pdf_bytes:
                st.download_button(
                    label="⬇ Télécharger le Rapport PDF",
                    data=pdf_bytes,
                    file_name=f"IntelliWatt_Rapport_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                save_archive(user["id"], user["username"], "pdf_export", "Tous",
                             {"type": "pdf", "timestamp": datetime.now().isoformat()})
                st.success("✅ Rapport PDF généré avec succès !")
            else:
                st.error("❌ reportlab non installé. Installez-le avec: pip install reportlab")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── History log ───────────────────────────────────────────
    st.markdown('<div class="content-card"><h3>📋 Historique des Archivages</h3>', unsafe_allow_html=True)
    log = get_archive_log(30)
    if log:
        log_data = [
            {"Date": r[6][:16] if r[6] else "", "Utilisateur": r[2], "Action": r[3], "Bâtiment": r[4]}
            for r in log
        ]
        st.dataframe(pd.DataFrame(log_data), use_container_width=True, hide_index=True, height=200)
    else:
        st.info("Aucun enregistrement pour l'instant.")
    st.markdown("</div>", unsafe_allow_html=True)
