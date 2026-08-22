"""Componentes reutilizables de UI y estilos globales para Streamlit."""
import streamlit as st


# ── Nombres de pasos del wizard ──────────────────────────────────────────────
STEP_LABELS = ["FUENTE", "GUION", "VISUAL", "MEDIA", "ARCHIVO"]


def inject_custom_css():
    """Inyecta el sistema de diseño ejecutivo de alto contraste."""
    st.markdown("""
    <style>
    /* ── Google Fonts ──────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Ocultar chrome nativo de Streamlit ────────────────────────────────── */
    header[data-testid="stHeader"],
    #MainMenu,
    .stDeployButton,
    [data-testid="stSidebarNav"],
    footer { display: none !important; }

    /* ── Tokens de diseño ──────────────────────────────────────────────────── */
    :root {
        --bg-base:        #0a0a10;
        --card-bg:        rgba(255, 255, 255, 0.05);
        --card-border:    rgba(255, 255, 255, 0.10);
        --card-hover:     rgba(255, 255, 255, 0.08);
        --accent:         #8B5CF6;
        --accent-dim:     rgba(139, 92, 246, 0.15);
        --accent-border:  rgba(139, 92, 246, 0.35);
        --gold:           #F59E0B;
        --success:        #10B981;
        --danger:         #EF4444;
        --text-primary:   #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted:     #6B7280;
        --radius:         12px;
        --radius-sm:      8px;
    }

    /* ── Tipografía global ─────────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
        background-color: var(--bg-base);
    }
    h1, h2, h3, h4, .stTitle {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        color: var(--text-primary) !important;
    }

    /* ── Fondo de la app ───────────────────────────────────────────────────── */
    .stApp { background-color: var(--bg-base); }

    /* ── Layout principal: espacio para el stepper fijo ───────────────────── */
    div.block-container {
        padding-top: 110px !important;
        padding-bottom: 40px !important;
        max-width: 860px !important;
        margin: 0 auto !important;
    }

    /* ── Cards ejecutivas ──────────────────────────────────────────────────── */
    .exec-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius);
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
    }
    .exec-card-accent {
        background: var(--accent-dim);
        border: 1px solid var(--accent-border);
        border-radius: var(--radius);
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── Título de sección dentro de cada paso ─────────────────────────────── */
    .step-section-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
    }

    /* ── Título principal del paso ─────────────────────────────────────────── */
    .step-main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 0 0.25rem 0;
        line-height: 1.2;
    }
    .step-subtitle {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin: 0 0 1.5rem 0;
    }

    /* ── Botón primario de acción ──────────────────────────────────────────── */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: var(--accent) !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.5rem !important;
        color: white !important;
        transition: opacity 0.15s ease !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.3) !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        opacity: 0.85 !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        transition: border-color 0.15s ease !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        border-color: var(--accent-border) !important;
        color: var(--text-primary) !important;
    }

    /* ── Inputs y selects ──────────────────────────────────────────────────── */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--accent-border) !important;
        box-shadow: 0 0 0 2px var(--accent-dim) !important;
    }

    /* ── Labels de formularios ─────────────────────────────────────────────── */
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stSlider"] label {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        color: var(--text-muted) !important;
    }

    /* ── Radio buttons ─────────────────────────────────────────────────────── */
    div[data-testid="stRadio"] > div {
        gap: 0.5rem;
    }

    /* ── Métricas ──────────────────────────────────────────────────────────── */
    div[data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-sm);
        padding: 1rem;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted) !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        color: var(--text-primary);
    }

    /* ── Expanders ─────────────────────────────────────────────────────────── */
    div[data-testid="stExpander"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-sm) !important;
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        color: var(--text-secondary) !important;
    }

    /* ── Info / Warning / Error boxes ──────────────────────────────────────── */
    div[data-testid="stAlert"] {
        border-radius: var(--radius-sm) !important;
        font-size: 0.875rem !important;
    }

    /* ── Progress bar ──────────────────────────────────────────────────────── */
    div[data-testid="stProgressBar"] > div > div {
        background: var(--accent) !important;
    }

    /* ── Timestamps de transcripción ───────────────────────────────────────── */
    .timestamp-tag {
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent);
        font-weight: 600;
        background: var(--accent-dim);
        padding: 2px 6px;
        border-radius: 4px;
        margin-right: 6px;
        font-size: 0.8rem;
    }

    /* ── Badges de estado ──────────────────────────────────────────────────── */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .badge-ok  { background: rgba(16,185,129,0.12); color: #10B981; border: 1px solid rgba(16,185,129,0.25); }
    .badge-warn{ background: rgba(245,158,11,0.12);  color: #F59E0B; border: 1px solid rgba(245,158,11,0.25); }
    .badge-err { background: rgba(239,68,68,0.12);   color: #EF4444; border: 1px solid rgba(239,68,68,0.25); }

    /* ── Separador ─────────────────────────────────────────────────────────── */
    hr { border-color: var(--card-border) !important; margin: 1.5rem 0 !important; }

    /* ── Tablas de guiones ─────────────────────────────────────────────────── */
    .script-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1rem 0;
        border-radius: var(--radius-sm);
        overflow: hidden;
        border: 1px solid var(--accent-border);
    }
    .script-table th {
        background: var(--accent-dim);
        color: var(--text-primary);
        padding: 10px 12px;
        font-family: 'Outfit', sans-serif;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        text-align: left;
        border-bottom: 1px solid var(--accent-border);
    }
    .script-table td {
        padding: 10px 12px;
        font-size: 0.85rem;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        vertical-align: top;
        color: var(--text-secondary);
    }
    .script-table tr:last-child td { border-bottom: none; }
    .script-table tr:nth-child(even) { background: rgba(255,255,255,0.012); }

    /* ── Cards de tweets ───────────────────────────────────────────────────── */
    .tweet-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-sm);
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .tweet-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-size: 0.78rem;
    }
    .tweet-body {
        font-size: 0.9rem;
        line-height: 1.55;
        color: var(--text-secondary);
        white-space: pre-wrap;
    }

    /* ── Cards de slides ───────────────────────────────────────────────────── */
    .slide-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-left: 3px solid var(--accent);
        border-radius: var(--radius-sm);
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }
    .slide-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }
    .slide-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        color: var(--text-primary);
    }
    .slide-stat {
        background: rgba(245,158,11,0.1);
        color: var(--gold);
        border: 1px solid rgba(245,158,11,0.25);
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        display: inline-block;
        margin-bottom: 0.4rem;
    }
    .slide-body {
        font-size: 0.84rem;
        color: var(--text-muted);
        line-height: 1.45;
    }

    /* ── Contenedor de visor scrolleable ───────────────────────────────────── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: var(--radius-sm) !important;
        border-color: var(--card-border) !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_stepper(current_step: int, completed_steps: list):
    """Renderiza el stepper horizontal de progreso fijo en la parte superior.

    Args:
        current_step: Índice del paso activo (0-4).
        completed_steps: Lista de índices de pasos ya completados.
    """
    steps_html = ""
    for i, label in enumerate(STEP_LABELS):
        is_active = (i == current_step)
        is_done = (i in completed_steps)

        if is_done:
            circle_style = "background:#10B981; border:2px solid #10B981; color:white;"
            icon = "✓"
            label_color = "#6B7280"
            line_color = "#10B981"
        elif is_active:
            circle_style = "background:#8B5CF6; border:2px solid #8B5CF6; color:white;"
            icon = str(i + 1)
            label_color = "#F8FAFC"
            line_color = "rgba(255,255,255,0.15)"
        else:
            circle_style = "background:transparent; border:2px solid rgba(255,255,255,0.18); color:#6B7280;"
            icon = str(i + 1)
            label_color = "#4B5563"
            line_color = "rgba(255,255,255,0.08)"

        label_weight = "700" if is_active else "400"
        label_size = "0.72rem" if is_active else "0.68rem"

        # Línea conectora entre pasos
        connector = ""
        if i < len(STEP_LABELS) - 1:
            next_is_done = (i + 1 in completed_steps) or (i + 1 == current_step and i in completed_steps)
            conn_color = "#10B981" if next_is_done else "rgba(255,255,255,0.10)"
            connector = f'<div style="flex:1; height:1px; background:{conn_color}; margin:0 6px; margin-top:-16px; align-self:flex-start; margin-top:16px;"></div>'

        steps_html += (
            f'<div style="display:flex; flex-direction:column; align-items:center; flex:1;">'
            f'<div style="{circle_style} width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:\'Outfit\',sans-serif; font-weight:700; font-size:0.8rem; flex-shrink:0;">'
            f'{icon}'
            f'</div>'
            f'<span style="margin-top:5px; font-size:{label_size}; font-weight:{label_weight}; letter-spacing:0.08em; text-transform:uppercase; color:{label_color}; font-family:\'Inter\',sans-serif; text-align:center;">'
            f'{label}'
            f'</span>'
            f'</div>'
            f'{connector}'
        )

    st.markdown(
        f'<div style="position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background: rgba(10,10,16,0.97); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.07); padding: 14px 5% 10px 5%; box-sizing: border-box;">'
        f'<div style="max-width:860px; margin:0 auto; display:flex; align-items:center; gap:0;">'
        f'{steps_html}'
        f'</div></div>',
        unsafe_allow_html=True
    )


def render_step_header(title: str, subtitle: str = ""):
    """Renderiza el encabezado limpio de cada paso del wizard."""
    sub_html = f'<p class="step-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <h1 class="step-main-title">{title}</h1>
    {sub_html}
    """, unsafe_allow_html=True)


def render_next_button(label: str, next_index: int, disabled: bool = False):
    """Botón estandarizado de avance al siguiente paso."""
    if st.button(label, type="primary", use_container_width=True, disabled=disabled):
        st.session_state["active_tab_index"] = next_index
        st.rerun()


def render_back_button(label: str, prev_index: int):
    """Botón estandarizado de retroceso al paso anterior."""
    if st.button(label, type="secondary", disabled=False):
        st.session_state["active_tab_index"] = prev_index
        st.rerun()


# ── Renderizadores de Guiones (sin cambios de lógica) ────────────────────────

def render_script_tiktok(data: dict):
    """Renderiza un guion técnico de TikTok/Reels en formato 2 columnas."""
    titulo = data.get("titulo", "Guion TikTok")
    duracion = data.get("duracion", 60)
    hook = data.get("hook_texto", "")
    cta = data.get("cta", "")
    hashtags = " ".join(data.get("hashtags", []))

    st.markdown(f"#### {titulo}")
    st.markdown(f"**Duración:** `{duracion}s` | **Formato:** `9:16 Vertical`")

    if hook:
        st.markdown(f"""
        <div style="background:rgba(139,92,246,0.08); border-left:3px solid #8B5CF6;
                    padding:8px 12px; border-radius:4px; margin-bottom:12px;">
            <strong style="color:#8B5CF6; font-size:0.78rem; text-transform:uppercase;
                           letter-spacing:0.06em;">Gancho (0-5s):</strong>
            <span style="color:#F1F5F9; font-style:italic;"> "{hook}"</span>
        </div>
        """, unsafe_allow_html=True)

    rows_html = []
    for s in data.get("slides", []):
        seg = s.get("seg", "")
        voz = s.get("voz", "")
        vis = s.get("visual", "")
        efe = s.get("efecto", "")
        rows_html.append(
f'''<tr>
<td><span class="timestamp-tag">{seg}</span></td>
<td><strong style="color:#F1F5F9;">{voz}</strong></td>
<td><span style="color:#94A3B8;">{vis}</span></td>
<td><span style="color:#F59E0B; font-size:0.75rem;">{efe}</span></td>
</tr>'''
        )

    table_html = f'''<table class="script-table">
<thead>
<tr>
<th style="width:15%;">Tiempo</th>
<th style="width:40%;">Locución</th>
<th style="width:30%;">Visual</th>
<th style="width:15%;">Efecto</th>
</tr>
</thead>
<tbody>{''.join(rows_html)}</tbody>
</table>'''
    st.markdown(table_html, unsafe_allow_html=True)

    if cta:
        st.markdown(f"**CTA:** {cta}")
    if hashtags:
        st.markdown(f"**Hashtags:** `{hashtags}`")


def render_script_twitter(data: dict):
    """Renderiza un hilo de X (Twitter) con preview de tweets."""
    titulo = data.get("titulo_hilo", "Hilo para X")
    tweets = data.get("tweets", [])
    total = data.get("total_tweets", len(tweets))
    gancho = data.get("gancho", "")
    cta = data.get("cta", "")
    hashtags = " ".join(data.get("hashtags", []))

    st.markdown(f"#### {titulo}")
    st.caption(f"Hilo en {total} tweets")

    if gancho:
        st.markdown(f"""
        <div style="background:rgba(139,92,246,0.08); border-left:3px solid #8B5CF6;
                    padding:8px 12px; border-radius:4px; margin-bottom:12px;">
            <strong style="color:#8B5CF6; font-size:0.78rem; text-transform:uppercase;
                           letter-spacing:0.06em;">Gancho:</strong>
            <span style="color:#F1F5F9; font-style:italic;"> "{gancho}"</span>
        </div>
        """, unsafe_allow_html=True)

    for idx, tw in enumerate(tweets, 1):
        num = tw.get("num", idx)
        texto = tw.get("texto", "")
        chars = len(texto)
        enfoque = tw.get("enfoque", "")
        badge_class = "badge-ok" if chars <= 280 else "badge-err"

        st.markdown(f"""
        <div class="tweet-card">
            <div class="tweet-header">
                <div>
                    <span style="font-weight:700; color:#8B5CF6;">Tweet {num}/{total}</span>
                    <span style="color:#6B7280; margin-left:8px; font-size:0.75rem;">{enfoque}</span>
                </div>
                <span class="badge {badge_class}">{chars}/280</span>
            </div>
            <div class="tweet-body">{texto}</div>
        </div>
        """, unsafe_allow_html=True)

    if cta:
        st.markdown(f"**Cierre / CTA:** {cta}")
    if hashtags:
        st.markdown(f"**Hashtags:** `{hashtags}`")


def render_script_social(data: dict, red: str = "instagram"):
    """Renderiza un carrusel P.A.S.C. para Instagram o Facebook."""
    titulo = data.get("titulo", "Carrusel PASC")
    slides = data.get("slides", [])
    total = data.get("total_slides", len(slides))
    copy_caption = data.get("copy_caption", "")
    hashtags = " ".join(data.get("hashtags", []))

    st.markdown(f"#### {titulo}")
    st.caption(f"Carrusel P.A.S.C. — {total} slides — {red.upper()}")

    for s in slides:
        num = s.get("slide_num", 1)
        tipo = s.get("tipo", "slide").upper()
        tit = s.get("titulo", "")
        cuerpo = s.get("cuerpo", "")
        dato = s.get("dato_destacado", "")
        stat_html = f'<div class="slide-stat">{dato}</div>' if dato else ""

        st.markdown(f"""
        <div class="slide-card">
            <div class="slide-header">
                <span class="slide-title">Slide {num} — {tit}</span>
                <span class="badge" style="background:rgba(139,92,246,0.12);
                      color:#8B5CF6; border:1px solid rgba(139,92,246,0.25);">[{tipo}]</span>
            </div>
            {stat_html}
            <div class="slide-body">{cuerpo}</div>
        </div>
        """, unsafe_allow_html=True)

    if copy_caption:
        st.markdown("##### Copy Caption")
        st.text_area("Caption:", value=copy_caption, height=100, disabled=True,
                     key=f"caption_{titulo[:10]}")
    if hashtags:
        st.markdown(f"**Hashtags:** `{hashtags}`")


def render_slide_card_preview(slide_num: int, title: str, body: str,
                               stat: str = "", subtitle: str = ""):
    """Renderiza una tarjeta de previsualización de slide."""
    stat_html = f'<div class="slide-stat">{stat}</div>' if stat else ""
    sub_html = (f'<div style="color:#F59E0B; font-size:0.75rem; '
                f'margin-bottom:3px;">{subtitle}</div>') if subtitle else ""
    st.markdown(f"""
    <div class="slide-card">
        <div class="slide-header">
            <span class="slide-title">#{slide_num}</span>
        </div>
        {sub_html}
        <strong style="color:#F8FAFC; font-size:0.9rem;">{title}</strong>
        {stat_html}
        <div class="slide-body" style="margin-top:4px;">{body}</div>
    </div>
    """, unsafe_allow_html=True)
