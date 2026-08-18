"""Pestaña 4: MEDIA — Cortador de Audio/Video y Subtítulos Sincronizados para CapCut."""
import os
import re
from pathlib import Path
import streamlit as st

from src.core.media_cutter import MediaCutter, format_timestamp_srt, format_timestamp_vtt
from src.core.audio_extractor import get_audio_info, check_ffmpeg
from src.config.settings import TEMP_DIR, OUTPUT_DIR


def parse_time_str(time_str: str) -> float:
    """Convierte una cadena en formato MM:SS, HH:MM:SS o segundos a float."""
    time_str = str(time_str).strip()
    if not time_str:
        return 0.0

    # Formato simple de segundos
    try:
        return max(0.0, float(time_str))
    except ValueError:
        pass

    # Formato HH:MM:SS o MM:SS
    parts = time_str.split(":")
    try:
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + float(s)
        elif len(parts) == 2:
            m, s = parts
            return int(m) * 60 + float(s)
    except (ValueError, TypeError):
        pass

    return 0.0


def format_time_str(seconds: float) -> str:
    """Convierte segundos a cadena formateada MM:SS o HH:MM:SS."""
    seconds = max(0.0, float(seconds))
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def filter_segments_by_range(segments: list[dict], start_sec: float, end_sec: float) -> list[dict]:
    """Filtra los segmentos de transcripción que caen dentro del rango especificado."""
    if not segments:
        return []
    filtered = []
    for s in segments:
        s_start = float(s.get("start", 0.0))
        s_end = float(s.get("end", 0.0))
        # Si hay solapamiento con el intervalo [start_sec, end_sec]
        if s_end > start_sec and s_start < end_sec:
            filtered.append(s)
    return filtered


def render_tab():
    """Renderiza la pestaña interactiva de corte de clips y subtitulado."""
    st.markdown("### ✂ Extractor de Clips y Subtítulos Dinámicos")
    st.caption("Corta fragmentos de video/audio sin pérdida de calidad y exporta subtítulos sincronizados listos para CapCut, TikTok o YouTube.")

    # 1. Recuperar contexto de sesión
    segments = st.session_state.get("segments", [])
    project_name = st.session_state.get("project_name", "conferencia_milei_01")
    source_file = (
        st.session_state.get("original_media_path")
        or st.session_state.get("source_file")
        or st.session_state.get("audio_path")
    )

    if "exported_media" not in st.session_state:
        st.session_state["exported_media"] = []

    # 2. Detección o Carga de Archivo Multimedia
    col_src1, col_src2 = st.columns([2, 1])

    with col_src1:
        if source_file and Path(source_file).exists():
            file_p = Path(source_file)
            size_mb = round(file_p.stat().st_size / (1024 * 1024), 2)
            st.success(f"Archivo multimedia activo: **{file_p.name}** ({size_mb} MB)")
        else:
            st.info("No hay un archivo multimedia activo desde la Pestaña 1. Puedes subir un video/audio aquí:")
            uploaded = st.file_uploader("Subir video o audio para corte:", type=["mp4", "mkv", "mov", "mp3", "wav", "m4a"])
            if uploaded:
                dest = TEMP_DIR / uploaded.name
                with open(dest, "wb") as f:
                    f.write(uploaded.getbuffer())
                source_file = str(dest)
                st.session_state["source_file"] = source_file
                st.session_state["original_media_path"] = source_file
                st.rerun()

    with col_src2:
        ffmpeg_available = check_ffmpeg()
        if ffmpeg_available:
            st.markdown('<div style="text-align: right; padding-top: 10px;"><span class="badge badge-ok">FFmpeg Activo</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: right; padding-top: 10px;"><span class="badge badge-err">FFmpeg No Detectado</span></div>', unsafe_allow_html=True)

    # 3. Cálculo de duración total
    max_duration = 120.0
    if segments:
        max_duration = max((float(s.get("end", 0.0)) for s in segments), default=120.0)
    elif source_file and Path(source_file).exists():
        info = get_audio_info(source_file)
        if info.get("duration", 0.0) > 0:
            max_duration = float(info["duration"])

    max_duration = max(5.0, max_duration)

    st.markdown("---")
    st.markdown("#### 1. Selección de Rango de Corte")

    # Inputs de tiempo y slider
    c_t1, c_t2, c_t3 = st.columns([1, 1, 2])
    with c_t1:
        inicio_str = st.text_input("Tiempo Inicio (MM:SS):", value="00:00", key="media_start_input")
    with c_t2:
        fin_def = format_time_str(min(60.0, max_duration))
        fin_str = st.text_input("Tiempo Fin (MM:SS):", value=fin_def, key="media_end_input")

    start_parsed = parse_time_str(inicio_str)
    end_parsed = parse_time_str(fin_str)

    if end_parsed <= start_parsed:
        end_parsed = min(start_parsed + 30.0, max_duration)

    with c_t3:
        rango_slider = st.slider(
            "Ajuste visual de rango (segundos):",
            min_value=0.0,
            max_value=max_duration,
            value=(min(start_parsed, max_duration), min(end_parsed, max_duration)),
            step=0.5
        )

    start_sec, end_sec = rango_slider
    duracion_clip = round(end_sec - start_sec, 2)

    # Previsualización del texto transcripto en el rango
    filtered_segs = filter_segments_by_range(segments, start_sec, end_sec)
    texto_rango = " ".join(s.get("text", "").strip() for s in filtered_segs if s.get("text"))

    st.markdown(f"**Duración seleccionada:** `{duracion_clip} s` ({format_time_str(start_sec)} ➔ {format_time_str(end_sec)}) | **Palabras:** `{len(texto_rango.split())}`")

    with st.expander("📝 Ver texto transcripto en el rango seleccionado", expanded=True):
        if texto_rango:
            st.markdown(f'<div class="glass-card" style="font-size: 0.9rem; line-height: 1.5; color: #F1F5F9;">"{texto_rango}"</div>', unsafe_allow_html=True)
        else:
            st.caption("No hay texto de transcripción sincronizado para este rango o no se ha realizado transcripción previa.")

    # 4. Opciones de Procesamiento
    st.markdown("#### 2. Opciones de Procesamiento")
    op_c1, op_c2, op_c3 = st.columns(3)
    with op_c1:
        opt_normalizar = st.checkbox("Normalizar audio (-16 LUFS)", value=True, help="Estándar para TikTok, Instagram y YouTube.")
    with op_c2:
        opt_silencios = st.checkbox("Eliminar pausas largas (>2s)", value=False, help="Remueve silencios muertos en la pista de audio.")
    with op_c3:
        opt_dinamico = st.checkbox("Ritmo Dinámico CapCut (3-5 pal/bloque)", value=True, help="Subtítulos cortos de alta retención para videos verticales.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Acciones de Corte y Exportación
    st.markdown("#### 3. Acciones de Exportación")
    act_col1, act_col2, act_col3, act_col4 = st.columns(4)

    cutter = MediaCutter()

    with act_col1:
        btn_cut_video = st.button("🎬 Cortar Video MP4", use_container_width=True, type="primary", disabled=(not bool(source_file)))
    with act_col2:
        btn_extract_audio = st.button("🎵 Extraer Audio MP3", use_container_width=True, disabled=(not bool(source_file)))
    with act_col3:
        btn_export_srt = st.button("📝 Subtítulos .SRT", use_container_width=True, disabled=(not bool(filtered_segs)))
    with act_col4:
        btn_export_vtt = st.button("🌐 Subtítulos .VTT", use_container_width=True, disabled=(not bool(filtered_segs)))

    # Lógica de Ejecución: Cortar Video
    if btn_cut_video and source_file:
        with st.spinner("Cortando fragmento de video con FFmpeg (-c copy)..."):
            try:
                nombre_clip = f"clip_{int(start_sec)}_{int(end_sec)}"
                res = cutter.cut_video(
                    source_path=source_file,
                    start_sec=start_sec,
                    end_sec=end_sec,
                    proyecto=project_name,
                    nombre=nombre_clip
                )

                # Generar subtítulos sincronizados correspondientes
                if filtered_segs:
                    srt_data = cutter.to_srt(filtered_segs, start_offset=start_sec, dynamic_rhythm=opt_dinamico)
                    srt_path = Path(res["path"]).with_suffix(".srt")
                    srt_path.write_text(srt_data, encoding="utf-8")
                    res["srt_path"] = str(srt_path)

                st.session_state["exported_media"].insert(0, {
                    "tipo": "video",
                    "nombre": f"{nombre_clip}.mp4",
                    "path": res["path"],
                    "duration": res["duration"],
                    "size_mb": res["size_mb"],
                    "srt_path": res.get("srt_path")
                })
                st.success(f"¡Clip cortado exitosamente! ({res['duration']}s | {res['size_mb']} MB)")
                st.rerun()
            except Exception as e:
                st.error(f"Error al cortar video: {str(e)}")

    # Lógica de Ejecución: Extraer Audio
    if btn_extract_audio and source_file:
        with st.spinner("Extrayendo pista de audio y normalizando a -16 LUFS..."):
            try:
                nombre_audio = f"audio_{int(start_sec)}_{int(end_sec)}"
                res = cutter.extract_audio(
                    source_path=source_file,
                    start_sec=start_sec,
                    end_sec=end_sec,
                    proyecto=project_name,
                    nombre=nombre_audio,
                    normalize=opt_normalizar,
                    remove_silence=opt_silencios
                )
                st.session_state["exported_media"].insert(0, {
                    "tipo": "audio",
                    "nombre": f"{nombre_audio}.mp3",
                    "path": res["path"],
                    "duration": res["duration"],
                    "size_mb": res["size_mb"]
                })
                st.success(f"¡Audio extraído con éxito! ({res['duration']}s | {res['size_mb']} MB)")
                st.rerun()
            except Exception as e:
                st.error(f"Error al extraer audio: {str(e)}")

    # Lógica de Ejecución: Exportar Subtítulos SRT
    if btn_export_srt and filtered_segs:
        srt_content = cutter.to_srt(filtered_segs, start_offset=start_sec, dynamic_rhythm=opt_dinamico)
        dest_dir = OUTPUT_DIR / project_name / "subtitulos"
        dest_dir.mkdir(parents=True, exist_ok=True)
        srt_file = dest_dir / f"subtitulos_{int(start_sec)}_{int(end_sec)}.srt"
        srt_file.write_text(srt_content, encoding="utf-8")

        st.session_state["exported_media"].insert(0, {
            "tipo": "subtitulos_srt",
            "nombre": srt_file.name,
            "path": str(srt_file),
            "content": srt_content,
            "duration": duracion_clip,
            "size_mb": round(len(srt_content.encode("utf-8")) / 1024, 2)
        })
        st.success("¡Subtítulos .SRT sincronizados generados con éxito!")
        st.rerun()

    # Lógica de Ejecución: Exportar Subtítulos VTT
    if btn_export_vtt and filtered_segs:
        vtt_content = cutter.to_vtt(filtered_segs, start_offset=start_sec, dynamic_rhythm=opt_dinamico)
        dest_dir = OUTPUT_DIR / project_name / "subtitulos"
        dest_dir.mkdir(parents=True, exist_ok=True)
        vtt_file = dest_dir / f"subtitulos_{int(start_sec)}_{int(end_sec)}.vtt"
        vtt_file.write_text(vtt_content, encoding="utf-8")

        st.session_state["exported_media"].insert(0, {
            "tipo": "subtitulos_vtt",
            "nombre": vtt_file.name,
            "path": str(vtt_file),
            "content": vtt_content,
            "duration": duracion_clip,
            "size_mb": round(len(vtt_content.encode("utf-8")) / 1024, 2)
        })
        st.success("¡Subtítulos WebVTT (.vtt) generados con éxito!")
        st.rerun()

    # 6. Historial de Recursos Exportados
    st.markdown("---")
    st.markdown("### 📦 Clips y Subtítulos Exportados en esta Sesión")

    exported = st.session_state.get("exported_media", [])

    if exported:
        for idx, item in enumerate(exported):
            item_path = Path(item["path"])
            item_type = item.get("tipo", "video")

            with st.container():
                st.markdown(f"#### 📁 {item['nombre']} (`{item.get('duration', 0)}s`)")
                
                exp_c1, exp_c2 = st.columns([2, 1])

                with exp_c1:
                    if item_type == "video" and item_path.exists():
                        st.video(str(item_path))
                    elif item_type == "audio" and item_path.exists():
                        st.audio(str(item_path))
                    elif "subtitulos" in item_type:
                        content_prev = item.get("content") or (item_path.read_text(encoding="utf-8") if item_path.exists() else "")
                        st.code(content_prev[:400] + ("..." if len(content_prev) > 400 else ""), language="text")

                with exp_c2:
                    st.caption(f"Tipo: `{item_type.upper()}` | Tamaño: `{item.get('size_mb', 0)} MB`")
                    if item_path.exists():
                        with open(item_path, "rb") as f_down:
                            mime_map = {
                                "video": "video/mp4",
                                "audio": "audio/mp3",
                                "subtitulos_srt": "text/plain",
                                "subtitulos_vtt": "text/vtt"
                            }
                            st.download_button(
                                label=f"📥 Descargar {item['nombre']}",
                                data=f_down.read(),
                                file_name=item["nombre"],
                                mime=mime_map.get(item_type, "application/octet-stream"),
                                key=f"dl_item_{idx}",
                                use_container_width=True
                            )
                        
                        if item.get("srt_path") and Path(item["srt_path"]).exists():
                            with open(item["srt_path"], "rb") as f_srt:
                                st.download_button(
                                    label=f"📝 Descargar Subtítulo Aliniado (.srt)",
                                    data=f_srt.read(),
                                    file_name=Path(item["srt_path"]).name,
                                    mime="text/plain",
                                    key=f"dl_srt_clip_{idx}",
                                    use_container_width=True
                                )

                st.markdown("<br>", unsafe_allow_html=True)

    else:
        st.info("Aún no has exportado clips o subtítulos en esta sesión. Selecciona un rango y haz clic en una de las acciones arriba.")
