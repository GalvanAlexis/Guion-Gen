"""Pestaña 1: FUENTE — Ingesta de Audio/Video y Transcripción."""
import streamlit as st

def render_tab():
    """Renderiza la pestaña de ingesta y transcripción."""
    st.markdown("### 🎙 Ingesta y Transcripción de Contenido")
    st.caption("Carga una conferencia, discurso, video de YouTube o pega texto para generar la transcripción con timestamps.")

    col1, col2 = st.columns([2, 1])

    with col1:
        project_name = st.text_input("Nombre del Proyecto:", value=st.session_state.get("project_name", "conferencia_milei_01"))
        st.session_state["project_name"] = project_name

        modo_ingesta = st.radio(
            "Origen del contenido:",
            ["📁 Subir archivo de video/audio", "🔗 URL de YouTube", "📝 Pegar texto plano"],
            horizontal=True
        )

        if "Subir archivo" in modo_ingesta:
            uploaded_file = st.file_uploader(
                "Arrastrá o seleccioná tu archivo multimedia:",
                type=["mp4", "mkv", "mov", "mp3", "wav", "m4a"],
                help="Soporta conferencias largas de hasta 50+ minutos."
            )
        elif "URL" in modo_ingesta:
            url_input = st.text_input("Pegá el enlace del video:", placeholder="https://www.youtube.com/watch?v=...")
        else:
            texto_directo = st.text_area("Pegá el texto completo de la transcripción:", height=200)

    with col2:
        st.markdown("#### Configuración de Motor")
        motor_whisper = st.selectbox(
            "Motor de Speech-to-Text:",
            ["Groq Whisper (Cloud - Ultra rápido ~60s)", "faster-whisper (Local CPU fallback)"]
        )
        idioma = st.selectbox("Idioma:", ["Español (es)", "Inglés (en)"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Iniciar Transcripción", use_container_width=True, type="primary"):
            st.info("Módulo de transcripción activo en ISS-002 / ISS-005.")

    st.markdown("---")
    st.markdown("#### Transcripción Generada")
    st.info("Carga un archivo o ingresa una URL arriba para ver los timestamps y bloques de texto generados.")
