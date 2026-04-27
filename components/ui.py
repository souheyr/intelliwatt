# components/ui.py
# Reusable HTML/widget helpers used across all pages


def metric_card(label: str, value: str, sub: str, color: str = "blue") -> str:
    return f"""<div class="metric-card {color}">
        <div class="mc-label">{label}</div>
        <div class="mc-value">{value}</div>
        <div class="mc-sub">{sub}</div>
    </div>"""


def status_badge(status: str) -> str:
    css_map = {
        "Actif":       "badge-active",
        "Critique":    "badge-critical",
        "Maintenance": "badge-maintenance",
    }
    css = css_map.get(status, "badge-active")
    return f'<span class="badge {css}">{status}</span>'


def load_pct(conso: float, capacite: float) -> float:
    return round((conso / capacite) * 100, 1)


def load_color(pct: float) -> str:
    if pct >= 90:
        return "#E53935"
    if pct >= 75:
        return "#FB8C00"
    return "#43A047"


def prog_bar(pct: float, color: str = "#1E88E5") -> str:
    return (
        f'<div class="prog-bar-bg">'
        f'<div class="prog-bar-fill" style="width:{min(pct,100)}%;background:{color};"></div>'
        f'</div>'
        f'<small style="color:#607D8B;font-size:0.74rem;">{pct}%</small>'
    )


def alert_box(msg: str, atype: str = "info") -> str:
    icons = {"danger": "⚠", "warning": "!", "info": "ℹ", "success": "✓"}
    icon = icons.get(atype, "i")
    return f'<div class="alert-box alert-{atype}"><strong>{icon}</strong> {msg}</div>'


def page_header(title: str, subtitle: str = "", meta: str = "") -> str:
    extra = (
        f'<div style="margin-top:8px;font-size:0.78rem;color:rgba(255,255,255,0.62);">{meta}</div>'
        if meta else ""
    )
    return (
        f'<div class="page-header">'
        f'<h1>{title}</h1><p>{subtitle}</p>{extra}'
        f'</div>'
    )
