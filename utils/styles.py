# utils/styles.py
# Injects global CSS (theme-aware)

import streamlit as st


def inject_css():
    theme = "light"
    if st.session_state.get("current_user"):
        theme = st.session_state.current_user.get("theme", "light")

    dark_vars = """
        --bg: #0D1B2A;
        --surface: #1A2C42;
        --surface2: #243347;
        --text: #E8F4FD;
        --neutral: #90A4AE;
        --blue-pale: #1A2C42;
        --shadow: rgba(0,0,0,0.4);
        --shadow-hover: rgba(0,0,0,0.6);
    """ if theme == "dark" else ""

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;600;700;800&display=swap');

    :root {{
        --blue-deep:  #0A2463;
        --blue-mid:   #1565C0;
        --blue-light: #1E88E5;
        --blue-pale:  #EBF4FF;
        --accent:     #00B4D8;
        --green:      #43A047;
        --red:        #E53935;
        --orange:     #FB8C00;
        --bg:         #F5F8FF;
        --surface:    #FFFFFF;
        --surface2:   #F8FBFF;
        --text:       #1A237E;
        --neutral:    #607D8B;
        --radius-sm:  8px;
        --radius-md:  14px;
        --radius-lg:  20px;
        --shadow:     rgba(10,36,99,0.08);
        --shadow-hover: rgba(10,36,99,0.18);
        {dark_vars}
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background: var(--bg) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0A2463 0%, #1565C0 60%, #1E88E5 100%) !important;
        border-right: none !important;
    }}
    [data-testid="stSidebar"] * {{
        color: rgba(255,255,255,0.92) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] .stSelectbox > div > div {{
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
    }}

    /* ---- LOGIN ---- */
    .login-container {{
        max-width:480px;margin:40px auto;background:var(--surface);
        border-radius:var(--radius-lg);padding:40px 44px;
        box-shadow:0 20px 60px rgba(10,36,99,0.15);
        border-top:4px solid var(--blue-light);
    }}
    .login-logo {{ text-align:center;margin-bottom:28px; }}
    .login-logo .l-icon {{ font-size:3rem;display:block;margin-bottom:8px; }}
    .login-logo h1 {{ font-family:'Syne',sans-serif!important;font-size:2.2rem;color:var(--blue-deep)!important;margin:0;font-weight:800; }}
    .login-logo p  {{ color:var(--neutral);font-size:0.85rem;margin:4px 0 0; }}

    /* ---- PAGE HEADER ---- */
    .page-header {{
        background:linear-gradient(135deg,#0A2463 0%,#1565C0 50%,#1E88E5 100%);
        border-radius:var(--radius-lg);padding:28px 36px;margin-bottom:24px;
        position:relative;overflow:hidden;
        box-shadow:0 8px 32px rgba(10,36,99,0.25);
    }}
    .page-header::before {{
        content:'';position:absolute;top:-60px;right:-60px;
        width:200px;height:200px;
        background:radial-gradient(circle,rgba(255,255,255,0.10) 0%,transparent 70%);
        border-radius:50%;
    }}
    .page-header h1 {{ font-family:'Syne',sans-serif!important;font-size:1.9rem!important;color:white!important;margin:0 0 4px!important;font-weight:800; }}
    .page-header p  {{ color:rgba(255,255,255,0.82)!important;margin:0!important;font-size:0.92rem; }}

    /* ---- METRIC CARDS ---- */
    .metric-card {{
        background:var(--surface);border-radius:var(--radius-md);padding:20px 18px;
        box-shadow:0 2px 16px var(--shadow);border-top:4px solid;
        transition:all 0.25s ease;position:relative;overflow:hidden;
    }}
    .metric-card:hover {{ box-shadow:0 6px 28px var(--shadow-hover);transform:translateY(-2px); }}
    .metric-card.blue   {{ border-color:var(--blue-light); }}
    .metric-card.red    {{ border-color:#E53935; }}
    .metric-card.green  {{ border-color:#43A047; }}
    .metric-card.teal   {{ border-color:var(--accent); }}
    .metric-card.orange {{ border-color:#FB8C00; }}
    .mc-label {{ font-size:0.73rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--neutral);font-weight:600;margin-bottom:8px; }}
    .mc-value {{ font-size:2.0rem;font-weight:700;line-height:1;margin-bottom:4px; }}
    .mc-sub   {{ font-size:0.78rem;color:#78909C; }}
    .metric-card.blue   .mc-value {{ color:var(--blue-light); }}
    .metric-card.red    .mc-value {{ color:#E53935; }}
    .metric-card.green  .mc-value {{ color:#43A047; }}
    .metric-card.teal   .mc-value {{ color:var(--accent); }}
    .metric-card.orange .mc-value {{ color:#FB8C00; }}

    /* ---- CONTENT CARD ---- */
    .content-card {{
        background:var(--surface);border-radius:var(--radius-md);
        padding:22px;box-shadow:0 2px 14px var(--shadow);margin-bottom:18px;
    }}
    .content-card h3 {{
        font-size:1.0rem;font-weight:700;color:var(--blue-deep);
        margin-bottom:16px;padding-bottom:10px;
        border-bottom:2px solid var(--blue-pale);
    }}

    /* ---- PROFILE CARD ---- */
    .profile-card {{
        background:linear-gradient(135deg,#0A2463,#1E88E5);border-radius:var(--radius-lg);
        padding:32px;text-align:center;color:white;
        position:relative;overflow:hidden;margin-bottom:20px;
    }}
    .profile-card .avatar {{ font-size:4rem;margin-bottom:12px; }}
    .profile-card .p-name {{ font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;margin-bottom:4px; }}
    .profile-card .p-role {{ font-size:0.85rem;opacity:0.8; }}
    .profile-card .p-badge {{
        display:inline-block;padding:4px 16px;
        background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.35);
        border-radius:20px;font-size:0.78rem;margin-top:10px;
    }}

    /* ---- DEVICE CONTROL ---- */
    .device-row {{
        background:var(--surface);border-radius:var(--radius-sm);padding:12px 16px;
        margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;
        box-shadow:0 1px 6px var(--shadow);border-left:4px solid;transition:all 0.2s;
    }}
    .device-on  {{ border-color:#43A047; }}
    .device-off {{ border-color:#B0BEC5;opacity:0.75; }}
    .device-icon {{ font-size:1.4rem;margin-right:10px; }}
    .device-name {{ font-weight:600;font-size:0.88rem;color:var(--text); }}
    .device-status {{ font-size:0.75rem;margin-top:2px; }}
    .status-on  {{ color:#43A047; }}
    .status-off {{ color:#90A4AE; }}

    /* ---- ADMIN TABLE ---- */
    .admin-user-row {{
        background:var(--surface);border-radius:var(--radius-sm);padding:14px 18px;
        margin-bottom:8px;display:flex;align-items:center;gap:16px;
        box-shadow:0 1px 8px var(--shadow);
    }}
    .admin-avatar {{ font-size:1.6rem; }}
    .admin-info .name   {{ font-weight:700;font-size:0.90rem;color:var(--text); }}
    .admin-info .detail {{ font-size:0.75rem;color:var(--neutral); }}
    .role-badge {{ display:inline-block;padding:3px 12px;border-radius:20px;font-size:0.72rem;font-weight:700; }}
    .role-admin {{ background:#E3F2FD;color:#1565C0;border:1px solid #90CAF9; }}
    .role-tech  {{ background:#E8F5E9;color:#2E7D32;border:1px solid #A5D6A7; }}

    /* ---- BADGES ---- */
    .badge {{ display:inline-block;padding:3px 12px;border-radius:20px;font-size:0.75rem;font-weight:600;letter-spacing:0.04em; }}
    .badge-critical    {{ background:#FFEBEE;color:#C62828;border:1px solid #EF9A9A; }}
    .badge-active      {{ background:#E8F5E9;color:#2E7D32;border:1px solid #A5D6A7; }}
    .badge-maintenance {{ background:#FFF3E0;color:#E65100;border:1px solid #FFCC02; }}
    .badge-pass {{ background:#E8F5E9;color:#2E7D32;border:1px solid #A5D6A7; }}
    .badge-fail {{ background:#FFEBEE;color:#C62828;border:1px solid #EF9A9A; }}

    /* ---- ALERT BOX ---- */
    .alert-box {{ border-radius:10px;padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:10px;font-size:0.87rem; }}
    .alert-danger  {{ background:#FFEBEE;border-left:4px solid #E53935;color:#B71C1C; }}
    .alert-warning {{ background:#FFF3E0;border-left:4px solid #FB8C00;color:#E65100; }}
    .alert-info    {{ background:#E3F2FD;border-left:4px solid #1E88E5;color:#0D47A1; }}
    .alert-success {{ background:#E8F5E9;border-left:4px solid #43A047;color:#1B5E20; }}

    /* ---- OPTIMISATION RESULTS ---- */
    .opt-before {{ background:#FFF3E0;border:1px solid #FFB74D;border-radius:10px;padding:16px;text-align:center; }}
    .opt-after  {{ background:#E8F5E9;border:1px solid #81C784;border-radius:10px;padding:16px;text-align:center; }}
    .opt-saving {{ background:linear-gradient(135deg,#0A2463,#1E88E5);border-radius:10px;padding:16px;text-align:center;color:white; }}
    .opt-before .val {{ font-size:2rem;font-weight:800;color:#E65100;display:block; }}
    .opt-after  .val {{ font-size:2rem;font-weight:800;color:#2E7D32;display:block; }}
    .opt-saving .val {{ font-size:2rem;font-weight:800;color:white;display:block; }}
    .opt-before .lbl,.opt-after .lbl {{ font-size:0.75rem;color:#555;margin-top:4px; }}
    .opt-saving .lbl {{ font-size:0.75rem;color:rgba(255,255,255,0.8);margin-top:4px; }}

    /* ---- PROGRESS BAR ---- */
    .prog-bar-bg   {{ background:#E3F2FD;border-radius:6px;height:8px;overflow:hidden;margin-top:6px; }}
    .prog-bar-fill {{ height:100%;border-radius:6px;transition:width 0.6s ease; }}

    /* ---- SCENARIO ROW ---- */
    .scenario-row {{ background:var(--surface);border-radius:10px;padding:16px;margin-bottom:10px;box-shadow:0 1px 8px var(--shadow);border-left:4px solid; }}
    .scenario-row.pass {{ border-color:#43A047; }}
    .scenario-row.fail {{ border-color:#E53935; }}
    .s-title {{ font-weight:700;color:var(--blue-deep);font-size:0.92rem; }}
    .s-param {{ font-size:0.78rem;color:#607D8B;margin-top:4px;font-family:monospace; }}

    /* ---- SETTINGS ---- */
    .setting-group {{
        background:var(--surface);border-radius:var(--radius-md);
        padding:22px;margin-bottom:16px;
        box-shadow:0 2px 12px var(--shadow);border-left:4px solid var(--blue-light);
    }}
    .setting-group h4 {{ font-weight:700;color:var(--blue-deep);margin-bottom:16px;font-size:0.95rem;display:flex;align-items:center;gap:8px; }}

    /* ---- NAV SIDEBAR ---- */
    .sidebar-logo {{ padding:16px 8px 18px;text-align:center; }}
    .logo-icon {{ width:54px;height:54px;background:rgba(255,255,255,0.15);border-radius:14px;display:inline-flex;align-items:center;justify-content:center;font-size:1.7rem;margin-bottom:8px;border:1px solid rgba(255,255,255,0.2); }}
    .logo-title {{ font-family:'Syne',sans-serif;font-size:1.45rem;font-weight:800;color:white!important;margin:0; }}
    .logo-sub {{ font-size:0.68rem;color:rgba(255,255,255,0.55)!important;text-transform:uppercase;letter-spacing:0.08em; }}
    .nav-section {{ font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.45)!important;padding:10px 4px 3px;margin-top:4px; }}
    .user-sidebar-card {{ background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.18);border-radius:12px;padding:11px 13px;margin:8px 0; }}
    .u-name {{ font-weight:700;font-size:0.88rem;color:white!important; }}
    .u-role {{ font-size:0.70rem;color:rgba(255,255,255,0.62)!important;margin-top:2px; }}

    /* ---- MISC ---- */
    #MainMenu {{ visibility:hidden; }}
    footer {{ visibility:hidden; }}
    header {{ visibility:hidden; }}
    .stDeployButton {{ display:none; }}
    .stButton > button {{
        background:linear-gradient(135deg,#1565C0,#1E88E5)!important;
        color:white!important;border:none!important;border-radius:10px!important;
        font-weight:600!important;padding:10px 22px!important;
        transition:all 0.2s!important;
        box-shadow:0 4px 14px rgba(21,101,192,0.3)!important;
    }}
    .stButton > button:hover {{ transform:translateY(-1px)!important;box-shadow:0 6px 20px rgba(21,101,192,0.5)!important; }}
    .stTabs [data-baseweb="tab"] {{ background:var(--blue-pale)!important;border-radius:8px 8px 0 0!important;color:var(--blue-mid)!important;font-weight:600!important;border:none!important;padding:8px 16px!important;font-size:0.84rem!important; }}
    .stTabs [aria-selected="true"] {{ background:var(--blue-light)!important;color:white!important; }}
    .stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {{
        border-radius:8px!important;border:1.5px solid #BBDEFB!important;
    }}
    .rtl {{ direction:rtl;text-align:right; }}
    </style>
    """, unsafe_allow_html=True)
