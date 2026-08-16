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
