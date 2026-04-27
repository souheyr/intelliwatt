# pages/profile.py

import streamlit as st
from utils.i18n import t
from utils.database import update_profile, update_password
from components.ui import page_header
from data.constants import BUILDINGS_DATA


def page_profile():
    user = st.session_state.current_user

    st.markdown(
        page_header(t("profile_title"), "Gérez vos informations personnelles et votre sécurité"),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])

    # ── Profile card ─────────────────────────────────────────
    with col1:
        b_assigned = "—"
        if user.get("building_assigned"):
            idx = (user["building_assigned"] or 1) - 1
            if 0 <= idx < len(BUILDINGS_DATA):
                b_assigned = BUILDINGS_DATA[idx]["nom"].split("—")[0].strip()

        st.markdown(f"""
        <div class="profile-card">
            <div class="avatar">{user.get('avatar','👤')}</div>
            <div class="p-name">{user['full_name']}</div>
            <div class="p-role">@{user['username']}</div>
            <div class="p-badge">{'🛡 Administrateur' if user['role']=='admin' else '🔧 Technicien'}</div>
        </div>
        <div class="content-card">
            <h3>ℹ️ Informations</h3>
            <table style="width:100%;font-size:0.86rem;border-collapse:collapse;">
                <tr><td style="padding:7px 0;color:#607D8B;">📧 Email</td><td>{user.get('email','—')}</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;">🏢 Bâtiment</td><td>{b_assigned}</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;">🌐 Langue</td><td>{user.get('language','fr').upper()}</td></tr>
                <tr><td style="padding:7px 0;color:#607D8B;">🎨 Thème</td><td>{user.get('theme','light').capitalize()}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # ── Edit tabs ─────────────────────────────────────────────
    with col2:
        tab_edit, tab_pass = st.tabs([f"✏️ {t('profile_edit')}", f"🔒 {t('profile_change_pass')}"])

        with tab_edit:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            avatars    = ["👤","👨‍💼","👩‍💼","👨‍🔧","👩‍🔧","👨‍🏫","👩‍🏫","👨‍💻","👩‍💻"]
            cur_av_idx = avatars.index(user.get("avatar","👤")) if user.get("avatar","👤") in avatars else 0

            with st.form("profile_edit_form"):
                new_name   = st.text_input("Nom complet", value=user["full_name"])
                new_email  = st.text_input("Email", value=user.get("email",""))
                new_avatar = st.selectbox("Avatar", avatars, index=cur_av_idx)

                if st.form_submit_button(t("save_changes"), use_container_width=True):
                    update_profile(user["id"], new_name, new_email, new_avatar)
                    st.session_state.current_user["full_name"] = new_name
                    st.session_state.current_user["email"]     = new_email
                    st.session_state.current_user["avatar"]    = new_avatar
                    st.success("✅ Profil mis à jour !")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_pass:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            with st.form("change_pass_form"):
                old_pass  = st.text_input(t("old_password"),     type="password")
                new_pass1 = st.text_input(t("new_password"),     type="password")
                new_pass2 = st.text_input(t("confirm_password"), type="password")

                if st.form_submit_button("🔒 Changer le Mot de Passe", use_container_width=True):
                    if not old_pass or not new_pass1 or not new_pass2:
                        st.error("Tous les champs sont obligatoires.")
                    elif new_pass1 != new_pass2:
                        st.error("Les nouveaux mots de passe ne correspondent pas.")
                    elif len(new_pass1) < 6:
                        st.error("Le mot de passe doit contenir au moins 6 caractères.")
                    else:
                        ok, msg = update_password(user["id"], old_pass, new_pass1)
                        st.success(f"✅ {msg}") if ok else st.error(msg)
            st.markdown("</div>", unsafe_allow_html=True)
    # ── Logout button (bottom-left) ─────────────────────────
    st.markdown("""
    <style>
    .logout-btn {
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 9999;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
