"""Pestaña 4: MEDIA — Cortador de Audio/Video y Subtítulos."""
import streamlit as st

def render_tab():
    """Renderiza la pestaña de corte de clips y exportación de subtítulos."""
    st.markdown("### ✂ Extractor de Clips y Subtítulos")
    st.caption("Corta fragmentos específicos del video/audio original y exporta subtítulos sincronizados .srt y .vtt para CapCut o YouTube.")

    st.markdown("#### Selección de Rango de Tiempo")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        inicio = st.text_input("Tiempo Inicio (MM:SS o segundos):", value="00:00")
    with col_t2:
        fin = st.text_input("Tiempo Fin (MM:SS o segundos):", value="01:00")

    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        normalizar = st.checkbox("Normalizar volumen a -16 LUFS (Estándar redes)", value=True)
    with col_opt2:
        silencio = st.checkbox("Eliminar pausas y silencios largos (>2s)", value=False)

    col_act1, col_act2, col_act3, col_act4 = st.columns(4)
    with col_act1:
        if st.button("🎬 Cortar Video MP4", use_container_width=True):
            st.info("Corte de video activo en ISS-014 / ISS-015.")
    with col_act2:
        if st.button("🎵 Extraer Audio MP3", use_container_width=True):
            st.info("Extracción de audio activo en ISS-014.")
    with col_act3:
        if st.button("📝 Subtítulos .SRT", use_container_width=True):
            st.info("Exportación .srt activa en ISS-014.")
    with col_act4:
        if st.button("🌐 Subtítulos .VTT", use_container_width=True):
            st.info("Exportación .vtt activa en ISS-014.")
