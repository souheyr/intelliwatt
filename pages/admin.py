
# ============================================================
# PAGE: ADMIN
# ============================================================
def page_admin():
    user = st.session_state.current_user
    if user["role"] != "admin":
        st.error("⛔ Accès refusé — Réservé aux administrateurs.")
        return
    
    st.markdown(page_header(t("admin_title"), "Gestion des utilisateurs, contrôles système et supervision globale"), unsafe_allow_html=True)
    
    tab_users, tab_system, tab_overview = st.tabs(["👥 Utilisateurs", "🖥️ Système", "📊 Vue Globale"])
    
    with tab_users:
        st.markdown('<div class="content-card"><h3>👥 Liste des Utilisateurs</h3>', unsafe_allow_html=True)
        
        users = get_all_users()
        for u in users:
            uid, uname, fname, email, role, b_assigned, avatar, created, last_login = u
            b_name = "—"
            if b_assigned and 1 <= int(b_assigned or 0) <= 8:
                b_name = BUILDINGS_DATA[int(b_assigned)-1]["nom"].split("—")[0].strip()
            
            last_str = last_login[:16] if last_login else "Jamais"
            
            st.markdown(f"""
            <div class="admin-user-row">
                <div class="admin-avatar">{avatar or '👤'}</div>
                <div class="admin-info" style="flex:1;">
                    <div class="name">{fname} <span style="color:#90A4AE;font-weight:400;">(@{uname})</span></div>
                    <div class="detail">📧 {email or '—'} | 🏢 {b_name} | 🕐 {last_str}</div>
                </div>
                <div>
                    <span class="role-badge {'role-admin' if role=='admin' else 'role-tech'}">
                        {'🛡 Admin' if role=='admin' else '🔧 Tech'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Create new user
        with st.expander("➕ Créer un Nouvel Utilisateur"):
            with st.form("admin_create_user"):
                c1, c2 = st.columns(2)
                with c1:
                    nu = st.text_input("Nom d'utilisateur *")
                    nf = st.text_input("Nom complet *")
                    ne = st.text_input("Email")
                with c2:
                    np1 = st.text_input("Mot de passe *", type="password")
                    nr = st.selectbox("Rôle", ["tech","admin"])
                    nav = st.selectbox("Avatar", ["👤","👨‍💼","👩‍💼","👨‍🔧","👩‍🔧"])
                nb = st.selectbox("Bâtiment assigné", range(1,9),
                                   format_func=lambda x: BUILDINGS_DATA[x-1]["nom"])
                
                if st.form_submit_button("➕ Créer", use_container_width=True):
                    if nu and nf and np1:
                        ok, msg = create_user(nu, np1, nf, ne, nr, nb, nav)
                        if ok:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Remplissez les champs obligatoires (*).")
    
    with tab_system:
        st.markdown('<div class="content-card"><h3>🖥️ État du Système</h3>', unsafe_allow_html=True)
        
        total_users = len(get_all_users())
        archive_count = len(get_archive_log(1000))
        
        sc = st.columns(4)
        with sc[0]: st.markdown(metric_card("Utilisateurs",str(total_users),"enregistrés","blue"),unsafe_allow_html=True)
        with sc[1]: st.markdown(metric_card("Archivages",str(archive_count),"enregistrements","teal"),unsafe_allow_html=True)
        with sc[2]: st.markdown(metric_card("Bâtiments","8","configurés","green"),unsafe_allow_html=True)
        with sc[3]: st.markdown(metric_card("Uptime","99.8%","30 derniers jours","orange"),unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Global device controls
        st.markdown("#### 🎛️ Contrôles Globaux — Tous Bâtiments")
        gc1, gc2, gc3 = st.columns(3)
        with gc1:
            if st.button("💡 Éclairage Général OFF", use_container_width=True, key="g_lights_off"):
                all_devs = get_device_controls()
                for dev in all_devs:
                    if dev[2] == "lumiere":
                        toggle_device(dev[0], 0, user["username"])
                st.success("✅ Tout l'éclairage éteint.")
        with gc2:
            if st.button("🔥 Chauffage Global OFF", use_container_width=True, key="g_heat_off"):
                all_devs = get_device_controls()
                for dev in all_devs:
                    if dev[2] == "chauffage":
                        toggle_device(dev[0], 0, user["username"])
                st.success("✅ Tout le chauffage éteint.")
        with gc3:
            if st.button("🚪 Portes LOCK", use_container_width=True, key="g_doors_lock"):
                all_devs = get_device_controls()
                for dev in all_devs:
                    if dev[2] == "porte":
                        toggle_device(dev[0], 0, user["username"])
                st.success("✅ Toutes les portes verrouillées.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab_overview:
        st.markdown('<div class="content-card"><h3>📊 Vue Globale des Consommations</h3>', unsafe_allow_html=True)
        
        total_conso = sum(b["conso"] for b in BUILDINGS_DATA)
        fig_ov = go.Figure(go.Bar(
            x=[b["nom"].split("—")[0].strip() for b in BUILDINGS_DATA],
            y=[b["conso"] for b in BUILDINGS_DATA],
            marker_color=["#E53935" if b["statut"]=="Critique" else "#1E88E5" if b["statut"]=="Actif" else "#FB8C00" for b in BUILDINGS_DATA],
            text=[f"{b['conso']} kWh" for b in BUILDINGS_DATA],
            textposition='outside',
        ))
        fig_ov.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=20),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(245,250,255,1)',
                              font=dict(family='Space Grotesk',size=11), yaxis_title="kWh/jour",
                              title=f"Total: {total_conso:,} kWh/jour", title_font_size=13)
        st.plotly_chart(fig_ov, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
