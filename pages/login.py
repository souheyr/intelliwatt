# pages/login.py
# Login & registration screens

import streamlit as st
from utils.database import verify_login, create_user
from utils.i18n import t
from data.constants import BUILDINGS_DATA


def page_login():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        if not st.session_state.show_register:
            _render_login_form()
        else:
            page_register()


def _render_login_form():
    st.markdown("""
    <div class="login-container">
        <div class="login-logo">
            <span class="l-icon">⚡</span>
            <h1>IntelliWatt</h1>
            <p>Université Batna 2 — Gestion Énergétique</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown(f"### 🔐 {t('login_title')}")
        username = st.text_input(t("login_user"), placeholder="ex: admin")
        password = st.text_input(t("login_pass"), type="password", placeholder="••••••••")
        col_btn, col_reg = st.columns(2)
        with col_btn:
            submit   = st.form_submit_button(t("login_btn"), use_container_width=True)
        with col_reg:
            register = st.form_submit_button(f"➕ {t('login_create')}", use_container_width=True)

        if submit:
            if not username or not password:
                st.error("Veuillez remplir tous les champs.")
            else:
                user = verify_login(username, password)
                if user:
                    # columns: id,username,pwd_hash,full_name,email,role,building_assigned,avatar,
                    #          created_at,last_login,theme,language,notifications
                    st.session_state.logged_in    = True
                    st.session_state.current_user = {
                        "id":                user[0],
                        "username":          user[1],
                        "full_name":         user[3],
                        "email":             user[4],
                        "role":              user[5],
                        "building_assigned": user[6],
                        "avatar":            user[7],
                        "theme":             user[10] or "light",
                        "language":          user[11] or "fr",
                        "notifications":     user[12],
                    }
                    st.session_state.lang = user[11] or "fr"
                    st.session_state.page = "dashboard"
                    st.success(f"Bienvenue {user[3]} !")
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")

        if register:
            st.session_state.show_register = True
            st.rerun()

    st.markdown("""
    <div style="text-align:center;margin-top:12px;font-size:0.78rem;color:#90A4AE;">
    Comptes démo: <code>admin</code> / <code>admin2024</code> | <code>tech01</code> / <code>tech1234</code>
    </div>
    """, unsafe_allow_html=True)


def page_register():
    st.markdown(f"### ➕ {t('register_title')}")

    avatars = ["👤", "👨‍💼", "👩‍💼", "👨‍🔧", "👩‍🔧", "👨‍🏫", "👩‍🏫", "👨‍💻", "👩‍💻"]

    with st.form("register_form"):
        col1, col2 = st.columns(2)

        with col1:
            new_username = st.text_input(t("login_user") + " *")
            new_fullname = st.text_input(t("reg_fullname") + " *")
            new_email    = st.text_input(t("reg_email"))

        with col2:
            new_password  = st.text_input(t("new_password") + " *", type="password")
            new_password2 = st.text_input(t("confirm_password") + " *", type="password")
            new_role      = st.selectbox(t("reg_role"), ["tech", "admin"])

        new_building = st.selectbox(
            t("reg_building"),
            range(1, 9),
            format_func=lambda x: BUILDINGS_DATA[x - 1]["nom"]
        )

        new_avatar = st.selectbox(t("reg_avatar"), avatars)

        col_sub, col_back = st.columns(2)

        with col_sub:
            submitted = st.form_submit_button(t("reg_btn"), use_container_width=True)

        with col_back:
            back = st.form_submit_button("← Retour", use_container_width=True)

    # ── SUBMIT REGISTER ─────────────────────────────
if submitted:

    if not new_username or not new_fullname or not new_password:
        st.error("Les champs marqués * sont obligatoires.")

    elif new_password != new_password2:
        st.error("Les mots de passe ne correspondent pas.")

    else:
        ok, msg = create_user(
            new_username,
            new_password,
            new_fullname,
            new_email,
            new_role,
        )

        if ok:
            # 🔥 تسجيل الدخول مباشرة بعد التسجيل
            st.session_state.logged_in = True
            st.session_state.current_user = {
                "username": new_username,
                "fullname": new_fullname,
                "role": new_role
            }

            st.success("Compte créé avec succès!")

            # 🔄 تحويل للتطبيق
            st.rerun()

        else:
            st.error(msg)
