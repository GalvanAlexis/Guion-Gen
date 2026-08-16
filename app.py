"""Guion-Gen: Fábrica de Guiones y Procesamiento Multimedia para Redes Sociales."""
import streamlit as st
from src.ui.components import inject_custom_css, render_header, render_footer_status
from src.ui.tab_fuente import render_tab as render_fuente
from src.ui.tab_guion import render_tab as render_guion
from src.ui.tab_visual import render_tab as render_visual
from src.ui.tab_media import render_tab as render_media
from src.ui.tab_biblioteca import render_tab as render_biblioteca
from src.config.settings import load_client_profile

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Guion-Gen — Fábrica de Contenido",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos de marca y dark mode
inject_custom_css()

# Cargar perfil de cliente por defecto
if "client" not in st.session_state:
    st.session_state["client"] = load_client_profile("lla_chascomus")

if "project_name" not in st.session_state:
    st.session_state["project_name"] = "conferencia_milei_01"

# Render de cabecera
render_header()

# Navegación en Barra Lateral
with st.sidebar:
    st.markdown("### 🧭 Navegación")
    selected_tab = st.radio(
        "Módulos de la Fábrica:",
        [
            "🎙 1. FUENTE (Ingesta)",
            "📄 2. GUION (Fábrica)",
            "🖼 3. VISUAL (Carruseles)",
            "✂ 4. MEDIA (Clips/Subs)",
            "📋 5. BIBLIOTECA (Historial)"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("### 🏢 Cliente Activo")
    st.markdown(f"**{st.session_state['client'].get('nombre', 'LLA Chascomús')}**")
    st.caption("Paleta: Violeta `#8B5CF6` / Oro `#F59E0B`")

    st.markdown("---")
    st.markdown("### ⚙ Configuración")
    st.caption("Guion-Gen v1.0 — Metodología SHDD")

# Renderizado de la pestaña seleccionada
if "1. FUENTE" in selected_tab:
    render_fuente()
elif "2. GUION" in selected_tab:
    render_guion()
elif "3. VISUAL" in selected_tab:
    render_visual()
elif "4. MEDIA" in selected_tab:
    render_media()
elif "5. BIBLIOTECA" in selected_tab:
    render_biblioteca()

# Render de barra de estado inferior
render_footer_status(gemini_ok=True, groq_ok=True, ffmpeg_ok=True)
