"""Pestaña 1: FUENTE — Ingesta de Audio/Video y Transcripción."""
import streamlit as st
from src.core.audio_extractor import extract_audio
from src.core.transcriber import transcribe, get_engine_status
from src.core.markdown_builder import build_markdown, format_timestamp
from src.config.settings import TEMP_DIR, OUTPUT_DIR
from src.ui.components import render_step_header, render_next_button
import json

def _auto_save_state(project_name):
    if not project_name:
        return
    state_to_save = {}
    keys_to_save = [
        "segments", "transcription_text", "markdown_content", 
        "transcription_stats", "project_name", "source_file", 
        "audio_path", "original_media_path", "topic_index"
    ]
    for k in keys_to_save:
        if k in st.session_state:
            state_to_save[k] = st.session_state[k]
    proj_dir = OUTPUT_DIR / project_name
    proj_dir.mkdir(parents=True, exist_ok=True)
    with open(proj_dir / "state.json", "w", encoding="utf-8") as f:
        json.dump(state_to_save, f, ensure_ascii=False)


def render_tab():
    """Renderiza el paso 1 del wizard: ingesta y transcripción."""
    render_step_header(
        "Cargá tu fuente",
        "Video, audio o texto — lo convertimos en una transcripción estructurada."
    )

    # ── Trabajos Recientes ───────────────────────────────────────────────────
    recent_projects = []
    if OUTPUT_DIR.exists():
        for proj_dir in OUTPUT_DIR.iterdir():
            if proj_dir.is_dir() and (proj_dir / "state.json").exists():
                recent_projects.append(proj_dir.name)
    
    if recent_projects:
        st.markdown('<p class="step-section-title">Trabajos Recientes</p>', unsafe_allow_html=True)
        col_rec1, col_rec2 = st.columns([3, 1])
        with col_rec1:
            recent_sel = st.selectbox("Cargar sesión", [""] + sorted(recent_projects, reverse=True), label_visibility="collapsed")
        with col_rec2:
            if st.button("Cargar", use_container_width=True) and recent_sel:
                with open(OUTPUT_DIR / recent_sel / "state.json", "r", encoding="utf-8") as f:
                    state_data = json.load(f)
                    for k, v in state_data.items():
                        st.session_state[k] = v
                st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Nombre del proyecto ───────────────────────────────────────────────────
    st.markdown('<p class="step-section-title">Proyecto</p>', unsafe_allow_html=True)
    project_name = st.text_input(
        "Nombre del proyecto",
        value=st.session_state.get("project_name", "conferencia_milei_01"),
        label_visibility="collapsed",
        placeholder="ej: conferencia_milei_01"
    )
    st.session_state["project_name"] = project_name

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Selección de origen ───────────────────────────────────────────────────
    st.markdown('<p class="step-section-title">Origen del contenido</p>', unsafe_allow_html=True)
    modo_ingesta = st.radio(
        "origen",
        ["Archivo multimedia", "URL de YouTube", "URL Web (Artículo/Texto)", "Texto directo"],
        horizontal=True,
        label_visibility="collapsed"
    )

    source_path = None
    source_type = None
    direct_text = None

    if "Archivo" in modo_ingesta:
        uploaded_file = st.file_uploader(
            "Arrastrá o seleccioná tu archivo (video o audio)",
            type=["mp4", "mkv", "mov", "webm", "mp3", "wav", "m4a"],
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            temp_upload_path = TEMP_DIR / uploaded_file.name
            with open(temp_upload_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            source_path = str(temp_upload_path)
            source_type = "file"
            st.success(f"`{uploaded_file.name}` cargado ({round(uploaded_file.size / (1024*1024), 2)} MB)")

    elif "YouTube" in modo_ingesta:
        url_input = st.text_input(
            "url",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed"
        )
        if url_input.strip():
            source_path = url_input.strip()
            source_type = "url"

    elif "URL Web" in modo_ingesta:
        url_input = st.text_input(
            "url_web",
            placeholder="https://es.wikipedia.org/wiki/Inteligencia_artificial",
            label_visibility="collapsed"
        )
        if url_input.strip():
            source_path = url_input.strip()
            source_type = "web_text"

    else:
        direct_text = st.text_area(
            "texto",
            height=160,
            placeholder="Pegá aquí el texto de la transcripción...",
            label_visibility="collapsed",
            key="fuente_direct_text"
        )
        if direct_text and direct_text.strip():
            source_type = "text"

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Configuración de motor ────────────────────────────────────────────────
    st.markdown('<p class="step-section-title">Motor de transcripción</p>', unsafe_allow_html=True)
    col_motor, col_lang = st.columns(2)

    with col_motor:
        engine_status = get_engine_status()
        motor_opciones = ["Auto (Groq → Local)"]
        if engine_status["groq_available"]:
            motor_opciones.append("Groq Whisper Cloud")
        motor_opciones.append("faster-whisper Local")
        motor_seleccionado = st.selectbox("Motor", motor_opciones, label_visibility="collapsed")

    with col_lang:
        idioma = st.selectbox("Idioma", ["Español (es)", "Inglés (en)"], label_visibility="collapsed")

    lang_code = "es" if "Español" in idioma else "en"
    engine_param = "auto"
    if "Groq" in motor_seleccionado:
        engine_param = "groq"
    elif "Local" in motor_seleccionado:
        engine_param = "local"

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botón principal de acción ─────────────────────────────────────────────
    btn_transcribir = st.button(
        "Transcribir",
        use_container_width=True,
        type="primary",
        disabled=(source_type is None)
    )

    # ── Pipeline de procesamiento ─────────────────────────────────────────────
    if btn_transcribir and source_type:
        progress_box = st.status("Procesando...", expanded=True)
        try:
            if source_type == "web_text":
                progress_box.write("Extrayendo texto de la web con Jina Reader...")
                from src.core.web_scraper import extract_text_from_url
                extracted_text = extract_text_from_url(source_path)
                progress_box.write("Estructurando texto extraído...")
                segments = [{"id": 0, "start": 0.0, "end": 0.0, "text": extracted_text}]
                trans_result = {
                    "engine_used": "Web Scraper",
                    "language": lang_code,
                    "elapsed_seconds": 0.5,
                    "total_segments": 1,
                    "total_words": len(extracted_text.split()),
                    "segments": segments,
                    "text": extracted_text
                }
            elif source_type == "text":
                progress_box.write("Estructurando texto directo...")
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
                progress_box.write("Extrayendo audio con FFmpeg...")
                audio_info = extract_audio(source_path, project_name=project_name)
                progress_box.write(f"Transcribiendo con {motor_seleccionado}...")
                trans_result = transcribe(audio_info["path"], language=lang_code, engine=engine_param)

            if source_type in ["text", "web_text"]:
                progress_box.write("Preparando documento Markdown...")
                md_content = trans_result["text"]
                
                # Guardar el md para consistencia
                project_dir = OUTPUT_DIR / project_name
                project_dir.mkdir(parents=True, exist_ok=True)
                with open(project_dir / "transcripcion.md", "w", encoding="utf-8") as f:
                    f.write(md_content)
            else:
                progress_box.write("Construyendo documento Markdown estructurado...")
                md_content = build_markdown(
                    trans_result["segments"],
                    project=project_name,
                    title=f"Transcripción — {project_name.replace('_', ' ').title()}",
                    engine_used=trans_result["engine_used"]
                )

            st.session_state["segments"] = trans_result["segments"]
            st.session_state["transcription_text"] = trans_result["text"]
            st.session_state["markdown_content"] = md_content
            st.session_state["transcription_stats"] = trans_result
            st.session_state["project_name"] = project_name
            st.session_state["source_file"] = source_path
            if source_type not in ["text", "web_text"]:
                st.session_state["audio_path"] = audio_info.get("path")
                if audio_info.get("original_file"):
                    st.session_state["original_media_path"] = audio_info.get("original_file")

            try:
                progress_box.write("Generando índice de temas...")
                if source_type in ["text", "web_text"]:
                    from src.core.script_generator import generate_topic_index_from_text
                    temas = generate_topic_index_from_text(md_content)
                else:
                    from src.core.script_generator import generate_topic_index
                    temas = generate_topic_index(md_content)
                st.session_state["topic_index"] = temas
            except Exception:
                pass

            _auto_save_state(project_name)
            progress_box.update(label="Transcripción completada", state="complete", expanded=False)
            st.rerun()

        except Exception as e:
            progress_box.update(label=f"Error: {str(e)}", state="error")

    # ── Resultados ────────────────────────────────────────────────────────────
    if "segments" in st.session_state and st.session_state["segments"]:
        st.markdown("---")
        stats = st.session_state.get("transcription_stats", {})
        segments = st.session_state["segments"]
        md_content = st.session_state.get("markdown_content", "")

        # Métricas
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Palabras", f"{stats.get('total_words', 0):,}")
        with m2:
            st.metric("Segmentos", len(segments))
        with m3:
            st.metric("Procesado en", f"{stats.get('elapsed_seconds', 0):.1f}s")

        st.markdown("<br>", unsafe_allow_html=True)

        # Acciones secundarias
        st.download_button(
            label="Descargar (.md)",
            data=md_content,
            file_name=f"transcripcion_{st.session_state.get('project_name', 'proyecto')}.md",
            mime="text/markdown",
            use_container_width=True
        )

        # Índice de temas
        topic_index = st.session_state.get("topic_index")
        if not topic_index:
            st.info("⚠️ El índice de temas no se generó (posible sesión antigua o error de conexión).")
            if st.button("Generar Índice Temático", use_container_width=True):
                with st.spinner("Generando índice temático..."):
                    try:
                        from src.core.script_generator import generate_topic_index
                        temas = generate_topic_index(md_content)
                        st.session_state["topic_index"] = temas
                        _auto_save_state(st.session_state.get("project_name"))
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

        if topic_index:
            # Compatibilidad con sesión anterior que pudo haber guardado el dict crudo
            if isinstance(topic_index, dict) and "data" in topic_index:
                topic_index = topic_index["data"]

            st.markdown("---")
            st.markdown('<p class="step-section-title">Índice de temas</p>', unsafe_allow_html=True)
            
            # Si a pesar de todo NO es iterable, lo forzamos a una lista vacía para evitar crasheos
            if not isinstance(topic_index, (list, tuple)):
                topic_index = []

            for t in topic_index:
                if isinstance(t, dict):
                    tema_txt = t.get("tema", "Tema")
                    if "preview" in t:
                        preview = t.get("preview", "")
                        st.markdown(f"**{tema_txt}**<br>_{preview}_", unsafe_allow_html=True)
                    else:
                        ts_list = t.get("timestamps") or [t.get("timestamp", "00:00")]
                        if isinstance(ts_list, list):
                            ts = ", ".join(ts_list)
                        else:
                            ts = str(ts_list)
                        st.markdown(f"`[{ts}]` {tema_txt}")
                else:
                    ts = "00:00"
                    tema_txt = str(t)
                    st.markdown(f"`[{ts}]` {tema_txt}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Visor de transcripción
        st.markdown('<p class="step-section-title">Vista previa (Editor Markdown)</p>', unsafe_allow_html=True)
        
        # Hacemos que la transcripción sea editable y guardamos el cambio
        transcripcion_editable = st.text_area(
            "Editor Markdown",
            value=st.session_state.get("markdown_content", ""),
            height=300,
            label_visibility="collapsed",
            key="fuente_markdown_editor"
        )
        
        if transcripcion_editable != st.session_state.get("markdown_content", ""):
            st.session_state["markdown_content"] = transcripcion_editable
            # Actualizamos también transcription_text para mantener sincronía básica
            st.session_state["transcription_text"] = transcripcion_editable
            
        st.markdown("<br>", unsafe_allow_html=True)

        # Botón de avance
        render_next_button("Generar guion →", next_index=1)

    else:
        st.markdown("""
        <div style="text-align:center; padding:3rem 1rem; color:#4B5563;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">🎙</div>
            <p style="font-size:0.9rem;">Cargá un archivo, pegá una URL o un texto para empezar.</p>
        </div>
        """, unsafe_allow_html=True)
