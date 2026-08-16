"""Pestaña 1: FUENTE — Ingesta de Audio/Video y Transcripción Completa."""
import os
import time
from pathlib import Path
import streamlit as st
from src.core.audio_extractor import extract_audio
from src.core.transcriber import transcribe, get_engine_status
from src.core.markdown_builder import build_markdown, format_timestamp
from src.config.settings import TEMP_DIR, OUTPUT_DIR

def render_tab():
    """Renderiza la pestaña de ingesta y transcripción."""
    st.markdown("### 🎙 Ingesta y Transcripción de Contenido")
    st.caption("Carga una conferencia, discurso, video de YouTube o pega texto para generar la transcripción estructurada con timestamps.")

    col1, col2 = st.columns([2, 1])

    with col1:
        project_name = st.text_input(
            "Nombre del Proyecto:",
            value=st.session_state.get("project_name", "conferencia_milei_01"),
            help="Se usará como identificador para guardar la transcripción y guiones."
        )
        st.session_state["project_name"] = project_name

        modo_ingesta = st.radio(
            "Origen del contenido:",
            ["📁 Subir archivo multimedia", "🔗 URL de YouTube", "📝 Pegar texto directo"],
            horizontal=True
        )

        source_path = None
        source_type = None
        direct_text = None

        if "Subir archivo" in modo_ingesta:
            uploaded_file = st.file_uploader(
                "Arrastrá o seleccioná tu archivo (video o audio):",
                type=["mp4", "mkv", "mov", "webm", "mp3", "wav", "m4a"],
                help="Soporta conferencias largas de 50+ minutos."
            )
            if uploaded_file is not None:
                # Guardar en temp
                temp_upload_path = TEMP_DIR / uploaded_file.name
                with open(temp_upload_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                source_path = str(temp_upload_path)
                source_type = "file"
                st.success(f"Archivo cargado: `{uploaded_file.name}` ({round(uploaded_file.size / (1024*1024), 2)} MB)")

        elif "URL" in modo_ingesta:
            url_input = st.text_input(
                "Pegá el enlace del video:",
                placeholder="https://www.youtube.com/watch?v=..."
            )
            if url_input.strip():
                source_path = url_input.strip()
                source_type = "url"

        else:
            direct_text = st.text_area(
                "Pegá el texto completo de la transcripción:",
                height=180,
                placeholder="Pegá aquí el texto si ya cuentas con una transcripción previa..."
            )
            if direct_text.strip():
                source_type = "text"

    with col2:
        st.markdown("#### Configuración de Motor")
        engine_status = get_engine_status()
        
        motor_opciones = ["Auto (Groq Cloud → Fallback Local)"]
        if engine_status["groq_available"]:
            motor_opciones.append("Groq Whisper Cloud (Ultra rápido)")
        motor_opciones.append("faster-whisper Local (CPU int8)")

        motor_seleccionado = st.selectbox("Motor Speech-to-Text:", motor_opciones)
        idioma = st.selectbox("Idioma del audio:", ["Español (es)", "Inglés (en)"])
        lang_code = "es" if "Español" in idioma else "en"

        engine_param = "auto"
        if "Groq" in motor_seleccionado:
            engine_param = "groq"
        elif "Local" in motor_seleccionado:
            engine_param = "local"

        st.markdown("<br>", unsafe_allow_html=True)
        btn_transcribir = st.button(
            "🚀 Iniciar Transcripción",
            use_container_width=True,
            type="primary",
            disabled=(source_type is None)
        )

    # Lógica de Ejecución del Pipeline
    if btn_transcribir and source_type:
        progress_box = st.status("Procesando contenido...", expanded=True)
        try:
            if source_type == "text":
                progress_box.write("Estructurando texto directo...")
                # Segmento único para texto directo
                segments = [{"id": 0, "start": 0.0, "end": 0.0, "text": direct_text.strip()}]
                trans_result = {
                    "engine_used": "Texto Directo",
                    "language": lang_code,
                    "elapsed_seconds": 0.1,
                    "total_segments": 1,
                    "total_words": len(direct_text.split()),
                    "segments": segments,
                    "text": direct_text.strip()
                }
            else:
                progress_box.write("1. Extrayendo y normalizando audio con FFmpeg a WAV mono 16 kHz...")
                audio_info = extract_audio(source_path, project_name=project_name)
                
                progress_box.write(f"2. Transcribiendo con {motor_seleccionado}...")
                trans_result = transcribe(
                    audio_info["path"],
                    language=lang_code,
                    engine=engine_param
                )

            progress_box.write("3. Construyendo documento Markdown estructurado...")
            md_content = build_markdown(
                trans_result["segments"],
                project=project_name,
                title=f"Transcripción — {project_name.replace('_', ' ').title()}",
                engine_used=trans_result["engine_used"]
            )

            # Persistir en session_state
            st.session_state["segments"] = trans_result["segments"]
            st.session_state["transcription_text"] = trans_result["text"]
            st.session_state["markdown_content"] = md_content
            st.session_state["transcription_stats"] = trans_result
            st.session_state["project_name"] = project_name

            progress_box.update(label="¡Transcripción completada con éxito!", state="complete", expanded=False)
            st.rerun()

        except Exception as e:
            progress_box.update(label=f"Error en el proceso: {str(e)}", state="error")
            st.error(f"Detalle del error: {str(e)}")

    # Sección de Resultados
    st.markdown("---")
    st.markdown("### 📋 Resultado de la Transcripción")

    if "segments" in st.session_state and st.session_state["segments"]:
        stats = st.session_state.get("transcription_stats", {})
        segments = st.session_state["segments"]
        md_content = st.session_state.get("markdown_content", "")
        
        # Tarjetas de Métricas
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Palabras", f"{stats.get('total_words', len(st.session_state.get('transcription_text', '').split())):,}")
        with m2:
            st.metric("Segmentos", len(segments))
        with m3:
            st.metric("Tiempo Proceso", f"{stats.get('elapsed_seconds', 0):.1f} s")
        with m4:
            st.metric("Motor Utilizado", stats.get("engine_used", "Groq Whisper"))

        # Acciones de Exportación
        act1, act2 = st.columns([1, 1])
        with act1:
            st.download_button(
                label="📥 Descargar Transcripción (.md)",
                data=md_content,
                file_name=f"transcripcion_{st.session_state.get('project_name', 'proyecto')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with act2:
            if st.button("➡️ Continuar a Fábrica de Guiones", use_container_width=True, type="secondary"):
                st.session_state["active_tab_index"] = 1
                st.rerun()

        # Visor Interactivo de Timestamps
        st.markdown("#### Vista Previa Segmentada")
        
        # Filtro por rango si hay múltiples segmentos con tiempos
        max_time = max((s.get("end", 0.0) for s in segments), default=0.0)
        if max_time > 10.0:
            rango = st.slider(
                "Filtrar por rango de tiempo (segundos):",
                min_value=0.0,
                max_value=max_time,
                value=(0.0, max_time),
                step=1.0
            )
            filtered_segments = [s for s in segments if s.get("end", 0.0) >= rango[0] and s.get("start", 0.0) <= rango[1]]
        else:
            filtered_segments = segments

        # Render de bloques con estilo Glass
        visor_container = st.container(height=350)
        with visor_container:
            for s in filtered_segments:
                start_ts = format_timestamp(s.get("start", 0.0))
                st.markdown(
                    f'<div style="margin-bottom: 8px;"><span class="timestamp-tag">{start_ts}</span> {s.get("text", "")}</div>',
                    unsafe_allow_html=True
                )

    else:
        st.info("No hay transcripción activa aún. Carga un archivo o ingresa una URL arriba para comenzar.")
