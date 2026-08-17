"""Componentes reutilizables de UI y estilos globales para Streamlit."""
import streamlit as st

def inject_custom_css():
    """Inyecta CSS personalizado para diseño oscuro ejecutivo y paleta LLA."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Variables de diseño */
    :root {
        --bg-base: #0a0a10;
        --bg-card: rgba(255, 255, 255, 0.03);
        --accent-primary: #8B5CF6;
        --accent-gold: #F59E0B;
        --accent-danger: #EF4444;
        --text-primary: #F8FAFC;
        --text-muted: #94A3B8;
        --border-glass: rgba(139, 92, 246, 0.18);
    }

    /* Fuentes globales */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }

    h1, h2, h3, h4, .stTitle {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Fondo general */
    .stApp {
        background-color: var(--bg-base);
    }

    /* Tarjetas con efecto Glassmorphism */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        border: 1px solid var(--border-glass);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    /* Badges de estado */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .badge-ok {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-warn {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-err {
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Timestamps en transcripción */
    .timestamp-tag {
        font-family: 'JetBrains Mono', monospace;
        color: #8B5CF6;
        font-weight: 600;
        background: rgba(139, 92, 246, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
        margin-right: 6px;
    }

    /* Barra de estado inferior */
    .status-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(10, 10, 16, 0.95);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(139, 92, 246, 0.2);
        padding: 6px 20px;
        font-size: 0.8rem;
        display: flex;
        justify-content: space-between;
        z-index: 999;
    }
    /* Estilos para renderizadores de guiones */
    .script-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    .script-table th {
        background: rgba(139, 92, 246, 0.15);
        color: #F8FAFC;
        padding: 10px 12px;
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        text-align: left;
        border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    }
    .script-table td {
        padding: 10px 12px;
        font-size: 0.85rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        vertical-align: top;
    }
    .script-table tr:last-child td {
        border-bottom: none;
    }
    .script-table tr:nth-child(even) {
        background: rgba(255, 255, 255, 0.015);
    }

    .tweet-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
    .tweet-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-size: 0.8rem;
    }
    .tweet-body {
        font-size: 0.9rem;
        line-height: 1.5;
        color: #F1F5F9;
        white-space: pre-wrap;
    }

    .slide-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(139, 92, 246, 0.18);
        border-left: 4px solid #8B5CF6;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
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
        font-size: 1rem;
        color: #F8FAFC;
    }
    .slide-stat {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 0.4rem;
    }
    .slide-body {
        font-size: 0.85rem;
        color: #CBD5E1;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Renderiza la cabecera principal de la aplicación."""
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(139,92,246,0.2); padding-bottom: 0.8rem; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: linear-gradient(135deg, #8B5CF6, #6D28D9); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-family: 'Outfit'; color: white;">G</div>
            <div>
                <h2 style="margin: 0; font-size: 1.4rem; color: #F8FAFC;">GUION-GEN</h2>
                <p style="margin: 0; font-size: 0.8rem; color: #94A3B8;">Fábrica de Contenido Político y Multimedia</p>
            </div>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <span class="badge badge-ok">LLA Chascomús</span>
            <span class="badge" style="background: rgba(139,92,246,0.15); color: #8B5CF6; border: 1px solid rgba(139,92,246,0.3);">v1.0 SHDD</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer_status(gemini_ok: bool = True, groq_ok: bool = True, ffmpeg_ok: bool = True):
    """Renderiza el estado de las herramientas en el pie."""
    st.markdown(f"""
    <div style="margin-top: 2rem; padding: 0.75rem 1rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(139,92,246,0.15); border-radius: 8px; display: flex; justify-content: space-between; font-size: 0.8rem; color: #94A3B8;">
        <div>
            <strong>Estado APIs:</strong> 
            <span style="color: {'#10B981' if gemini_ok else '#EF4444'}; margin-left: 8px;">● Gemini Flash</span>
            <span style="color: {'#10B981' if groq_ok else '#EF4444'}; margin-left: 12px;">● Groq LLaMA/Whisper</span>
            <span style="color: {'#10B981' if ffmpeg_ok else '#EF4444'}; margin-left: 12px;">● FFmpeg Audio</span>
        </div>
        <div>
            <span>Motor activo: <strong>Híbrido (Groq + Gemini)</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_script_tiktok(data: dict):
    """Renderiza un guion técnico de TikTok/Reels en formato 2 columnas."""
    titulo = data.get("titulo", "Guion TikTok")
    duracion = data.get("duracion", 60)
    hook = data.get("hook_texto", "")
    cta = data.get("cta", "")
    hashtags = " ".join(data.get("hashtags", []))

    st.markdown(f"#### 🎬 {titulo}")
    st.markdown(f"**Duración:** `{duracion}s` | **Formato:** `9:16 Vertical`")

    if hook:
        st.markdown(f"""
        <div style="background: rgba(139,92,246,0.1); border-left: 4px solid #8B5CF6; padding: 8px 12px; border-radius: 4px; margin-bottom: 12px;">
            <strong style="color: #8B5CF6;">Gancho Inicial (0-5s):</strong> <em>"{hook}"</em>
        </div>
        """, unsafe_allow_html=True)

    rows_html = []
    for s in data.get("slides", []):
        seg = s.get("seg", "")
        voz = s.get("voz", "")
        vis = s.get("visual", "")
        efe = s.get("efecto", "")
        rows_html.append(f"""
        <tr>
            <td><span class="timestamp-tag">{seg}</span></td>
            <td><strong>{voz}</strong></td>
            <td><span style="color: #94A3B8;">{vis}</span></td>
            <td><span style="color: #F59E0B; font-size: 0.75rem;">{efe}</span></td>
        </tr>
        """)

    table_html = f"""
    <table class="script-table">
        <thead>
            <tr>
                <th style="width: 15%;">Tiempo</th>
                <th style="width: 40%;">Locución (VOZ)</th>
                <th style="width: 30%;">Visual / B-Roll</th>
                <th style="width: 15%;">Efecto / Audio</th>
            </tr>
        </thead>
        <tbody>
            {''.join(rows_html)}
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    if cta:
        st.markdown(f"**Llamado a la acción (CTA):** {cta}")
    if hashtags:
        st.markdown(f"**Hashtags:** `{hashtags}`")

def render_script_twitter(data: dict):
    """Renderiza un hilo de X (Twitter) con preview de tweets y contador de caracteres."""
    titulo = data.get("titulo_hilo", "Hilo para X")
    tweets = data.get("tweets", [])
    total = data.get("total_tweets", len(tweets))
    gancho = data.get("gancho", "")
    cta = data.get("cta", "")
    hashtags = " ".join(data.get("hashtags", []))

    st.markdown(f"#### 🧵 {titulo}")
    st.caption(f"Hilo estructurado en {total} tweets")

    if gancho:
        st.markdown(f"""
        <div style="background: rgba(139,92,246,0.1); border-left: 4px solid #8B5CF6; padding: 8px 12px; border-radius: 4px; margin-bottom: 12px;">
            <strong style="color: #8B5CF6;">Gancho de Apertura:</strong> <em>"{gancho}"</em>
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
                    <span style="font-weight: 700; color: #8B5CF6;">Tweet {num}/{total}</span>
                    <span style="color: #94A3B8; margin-left: 8px;">({enfoque})</span>
                </div>
                <span class="badge {badge_class}">{chars} / 280 caracteres</span>
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

    st.markdown(f"#### 🖼 {titulo}")
    st.caption(f"Carrusel P.A.S.C. ({total} Diapositivas 4:5 para {red.upper()})")

    for s in slides:
        num = s.get("slide_num", 1)
        tipo = s.get("tipo", "slide").upper()
        tit = s.get("titulo", "")
        cuerpo = s.get("cuerpo", "")
        dato = s.get("dato_destacado", "")

        stat_html = f'<div class="slide-stat">{dato}</div>' if dato else ''

        st.markdown(f"""
        <div class="slide-card">
            <div class="slide-header">
                <span class="slide-title">Slide {num} — {tit}</span>
                <span class="badge" style="background: rgba(139,92,246,0.2); color: #8B5CF6;">[{tipo}]</span>
            </div>
            {stat_html}
            <div class="slide-body">{cuerpo}</div>
        </div>
        """, unsafe_allow_html=True)

    if copy_caption:
        st.markdown("##### ✍️ Copy Caption para Publicación")
        st.text_area("Caption de publicación:", value=copy_caption, height=120, disabled=True, key=f"caption_{titulo[:10]}")

    if hashtags:
        st.markdown(f"**Hashtags:** `{hashtags}`")

