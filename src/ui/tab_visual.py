"""Pestaña 3: VISUAL — Generador de Carruseles e Imágenes."""
import streamlit as st

def render_tab():
    """Renderiza la pestaña de generación de carruseles e imágenes."""
    st.markdown("### 🖼 Generador Visual de Carruseles y Portadas")
    st.caption("Crea piezas gráficas 4:5 y 9:16 con plantillas CSS LLA o fondos generados por IA.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Configuración Visual")
        modo_visual = st.radio(
            "Modo de renderizado:",
            ["⚡ Modo CSS Rápido (Plantillas LLA)", "🎨 Modo IA Creativa (Fondos Gemini)"],
            horizontal=True
        )

        plantilla = st.selectbox(
            "Plantilla de diseño:",
            ["LLA Dark (Violeta + Oro)", "Alerta Roja (Urgente / Denuncia)", "Estadística (Datos / Tablas)"]
        )

        formato = st.selectbox(
            "Formato de exportación:",
            ["Carrusel 4:5 (1080x1350 - Instagram)", "Story/Reel 9:16 (1080x1920)", "Cuadrado 1:1 (1080x1080)"]
        )

        if st.button("🖼 Renderizar Diapositivas", use_container_width=True, type="primary"):
            st.info("Renderizado de carruseles activo en ISS-011 / ISS-013.")

    with col2:
        st.markdown("#### Previsualización de Slides")
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2rem;">
            <p style="color: #94A3B8;">Los slides generados se mostrarán en esta cuadrícula con opción de descarga individual o paquete ZIP.</p>
        </div>
        """, unsafe_allow_html=True)
