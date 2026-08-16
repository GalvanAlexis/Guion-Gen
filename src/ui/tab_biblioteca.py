"""Pestaña 5: BIBLIOTECA — Historial y Gestión de Proyectos."""
import streamlit as st

def render_tab():
    """Renderiza la pestaña de biblioteca de proyectos."""
    st.markdown("### 📋 Biblioteca de Proyectos e Historial")
    st.caption("Consulta el archivo histórico de conferencias transcriptas, guiones generados y carruseles creados.")

    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    with col_s1:
        st.text_input("🔍 Buscar proyecto o palabra clave:", placeholder="Buscar por tema, fecha o etiqueta...")
    with col_s2:
        st.selectbox("Filtrar por Red:", ["Todas", "TikTok", "X", "Instagram", "Facebook"])
    with col_s3:
        st.selectbox("Filtrar por Etiqueta:", ["Todas", "Milei", "LLA", "Economía", "Seguridad"])

    st.markdown("---")
    st.info("No hay proyectos previos registrados aún. Los proyectos completados se guardarán automáticamente en output/.")
