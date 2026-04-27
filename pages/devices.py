# pages/devices.py

import streamlit as st
from utils.i18n import t
from utils.database import get_device_controls, toggle_device
from components.ui import alert_box, page_header
from data.constants import BUILDINGS_DATA


DEVICE_ICONS = {
    "lumiere":   "💡",
    "porte":     "🚪",
    "fenetre":   "🪟",
    "chauffage": "🔥",
    "clim":      "❄️",
}

TYPE_LABELS = {
    "lumiere":   "💡 Éclairage",
    "porte":     "🚪 Portes",
    "fenetre":   "🪟 Fenêtres",
    "chauffage": "🔥 Chauffage",
    "clim":      "❄️ Climatisation",
}


def page_devices():
    user     = st.session_state.current_user
    is_admin = user["role"] == "admin"

    st.markdown(page_header(t("devices_title"), t("devices_subtitle")), unsafe_allow_html=True)

    # ── Building selection ────────────────────────────────────
    if is_admin:
        building_options = {b["nom"]: b["id"] for b in BUILDINGS_DATA}
        selected_bld     = st.selectbox("Sélectionner le bâtiment", list(building_options.keys()))
        b_id             = building_options[selected_bld]
    else:
        b_id   = user.get("building_assigned", 1) or 1
        b_name = next((b["nom"] for b in BUILDINGS_DATA if b["id"] == b_id), "Bâtiment 1")
        st.markdown(alert_box(f"Accès limité : {b_name}", "info"), unsafe_allow_html=True)

    devices = get_device_controls(b_id)
    if not devices:
        st.warning("Aucun appareil configuré pour ce bâtiment.")
        return

    # ── Global controls ───────────────────────────────────────
    st.markdown('<div class="content-card"><h3>🎛️ Contrôles Globaux</h3>', unsafe_allow_html=True)
    gcol1, gcol2, gcol3, gcol4 = st.columns(4)
    with gcol1:
        if st.button("💡 Tout Allumer", use_container_width=True, key="all_on"):
            for dev in devices:
                toggle_device(dev[0], 1, user["username"])
            st.success("Tous les appareils allumés.")
            st.rerun()
    with gcol2:
        if st.button("🌙 Tout Éteindre", use_container_width=True, key="all_off"):
            for dev in devices:
                toggle_device(dev[0], 0, user["username"])
            st.success("Tous les appareils éteints.")
            st.rerun()
    with gcol3:
        if st.button("💡 Lights OFF", use_container_width=True, key="lights_off"):
            for dev in devices:
                if dev[2] == "lumiere":
                    toggle_device(dev[0], 0, user["username"])
            st.success("Éclairage éteint.")
            st.rerun()
    with gcol4:
        if st.button("🔥 Chauffage OFF", use_container_width=True, key="heat_off"):
            for dev in devices:
                if dev[2] == "chauffage":
                    toggle_device(dev[0], 0, user["username"])
            st.success("Chauffage éteint.")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Device rows grouped by type ───────────────────────────
    device_by_type: dict[str, list] = {}
    for dev in devices:
        dtype = dev[2]
        device_by_type.setdefault(dtype, []).append(dev)

    for dtype, devs in device_by_type.items():
        label = TYPE_LABELS.get(dtype, dtype)
        st.markdown(f'<div class="content-card"><h3>{label}</h3>', unsafe_allow_html=True)

        for dev in devs:
            # dev = (id, building_id, device_type, device_name, status, last_updated, updated_by)
            dev_id, _, _, dev_name, status, last_upd, upd_by = dev
            icon       = DEVICE_ICONS.get(dtype, "🔌")
            row_class  = "device-on" if status else "device-off"
            stat_label = t("device_on") if status else t("device_off")
            stat_class = "status-on"   if status else "status-off"

            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.markdown(f"""
                <div class="device-row {row_class}">
                    <span class="device-icon">{icon}</span>
                    <div>
                        <div class="device-name">{dev_name}</div>
                        <div class="device-status {stat_class}">{stat_label} · {last_upd[:16] if last_upd else '—'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                btn_label = "🔴 OFF" if status else "🟢 ON"
                if st.button(btn_label, key=f"toggle_{dev_id}", use_container_width=True):
                    toggle_device(dev_id, 0 if status else 1, user["username"])
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
