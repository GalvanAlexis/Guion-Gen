"""Pestaña 2: GUION — Fábrica de Guiones Multicanal."""
import streamlit as st
from src.core.script_generator import generate_script, slugify
from src.ui.components import (
    render_step_header, render_next_button, render_back_button,
    render_script_tiktok, render_script_twitter, render_script_social
)
from src.config.settings import load_client_profile


def render_tab():
    """Renderiza el paso 2 del wizard: generación de guiones."""
    render_step_header(
        "Generá el guion",
        "Elegí la plataforma, el tono y dejá que la IA construya el guion."
    )

    segments = st.session_state.get("segments", [])
    transcription_text = st.session_state.get("transcription_text", "")
    project_name = st.session_state.get("project_name", "conferencia_milei_01")
    cliente = st.session_state.get("client", load_client_profile("lla_chascomus"))

    # ── Sin fuente cargada ────────────────────────────────────────────────────
    if not segments and not transcription_text:
        st.markdown("""
        <div style="text-align:center; padding:2rem 1rem; color:#4B5563;">
            <p style="font-size:0.9rem;">Primero necesitás una transcripción.</p>
        </div>
        """, unsafe_allow_html=True)

        col_btn, col_txt = st.columns([1, 2])
        with col_btn:
            render_back_button("← Volver a Fuente", prev_index=0)
        with col_txt:
            direct_input = st.text_area(
                "O pegá texto directo:",
                height=100,
                placeholder="Pegá un fragmento de discurso aquí...",
                key="guion_direct_input"
            )
            if direct_input.strip():
                transcription_text = direct_input.strip()
                st.session_state["transcription_text"] = transcription_text

    # ── Columnas de configuración y preview ───────────────────────────────────
    col_cfg, col_res = st.columns([1, 1], gap="large")

    # Columna Izquierda: Configuración
    with col_cfg:
        st.markdown('<p class="step-section-title">Configuración</p>', unsafe_allow_html=True)

        formato_general = st.radio(
            "Formato",
            ["Video (Clips)", "Imagen / Texto"],
            horizontal=True,
            label_visibility="collapsed"
        )

        if "Video" in formato_general:
            red_opciones = {"TikTok / Reels / Shorts (9:16)": "tiktok"}
        else:
            red_opciones = {
                "Instagram (Carrusel P.A.S.C.)": "instagram",
                "X / Twitter (Hilo Viral)": "x",
                "Facebook (Carrusel)": "facebook"
            }

        red_label = st.selectbox("Plataforma", list(red_opciones.keys()),
                                  label_visibility="collapsed")
        red_code = red_opciones[red_label]

        tono_opciones = {
            "Confrontacional / Alerta": "confrontacional",
            "Educativo / Datos duros": "educativo",
            "Urgente / Denuncia": "urgente",
            "Motivacional": "motivacional"
        }
        if "Video" in formato_general:
            tono_opciones["Libre"] = "libre"

        tono_label = st.selectbox("Tono", list(tono_opciones.keys()),
                                   label_visibility="collapsed")
        tono_code = tono_opciones[tono_label]

        topic_index = st.session_state.get("topic_index", [])
        if isinstance(topic_index, dict) and "data" in topic_index:
            topic_index = topic_index["data"]
        if not isinstance(topic_index, list):
            topic_index = []

        st.markdown('<p style="font-size:0.8rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; margin-bottom:0.5rem;">Índice de Temas</p>', unsafe_allow_html=True)
        
        selected_topics_info = []
        if topic_index:
            with st.container(height=250, border=True):
                for idx, t in enumerate(topic_index):
                    if isinstance(t, dict):
                        ts_list = t.get("timestamps") or [t.get("timestamp", "00:00")]
                        ts = ", ".join(ts_list) if isinstance(ts_list, list) else str(ts_list)
                        tema_label = f"[{ts}] {t.get('tema', '')}"
                    else:
                        tema_label = str(t)
                        ts = "00:00"
                    
                    is_checked = st.checkbox(tema_label, key=f"chk_tema_{idx}")
                    if is_checked:
                        selected_topics_info.append({
                            "label": tema_label,
                            "tema": t.get("tema", "") if isinstance(t, dict) else str(t),
                            "timestamps": t.get("timestamps") or [t.get("timestamp", "00:00")] if isinstance(t, dict) else ["00:00"]
                        })
        else:
            st.info("No hay índice de temas disponible.")

        # Fallback manual
        temas_sugeridos = cliente.get("temas_frecuentes", [])
        if not selected_topics_info:
            tema_seleccionado = st.selectbox(
                "Tema Manual / Sugerido",
                ["[Libre]"] + temas_sugeridos,
                label_visibility="collapsed"
            )
            if tema_seleccionado == "[Libre]":
                tema_final = st.text_input(
                    "Tema específico",
                    placeholder="Ej: Déficit fiscal heredado vs superávit",
                    label_visibility="collapsed"
                )
            else:
                tema_final = st.text_input("Tema", value=tema_seleccionado, label_visibility="collapsed")
        else:
            tema_final_str = " | ".join([info["tema"] for info in selected_topics_info])
            tema_final = st.text_input("Tema seleccionado", value=tema_final_str, disabled=True, label_visibility="collapsed")

        # Rango de transcripción
        def parse_ts(ts_str):
            parts = ts_str.strip().split(":")
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            return 0.0

        def parse_ts_range(ts_range_str):
            parts = ts_range_str.split("-")
            if len(parts) == 2:
                return parse_ts(parts[0]), parse_ts(parts[1])
            else:
                s = parse_ts(parts[0])
                return s, s + 60.0

        texto_a_usar = transcription_text
        preview_segments = []
        if segments:
            if selected_topics_info:
                valid_ranges = []
                for info in selected_topics_info:
                    for ts_str in info["timestamps"]:
                        valid_ranges.append(parse_ts_range(ts_str))
                
                filtered = []
                for s in segments:
                    s_mid = (s.get("start", 0.0) + s.get("end", 0.0)) / 2
                    if any(r_start <= s_mid <= r_end for r_start, r_end in valid_ranges):
                        filtered.append(s)
                
                if filtered:
                    texto_a_usar = " ".join([s.get("text", "") for s in filtered]).strip()
                else:
                    texto_a_usar = ""
                preview_segments = filtered
            else:
                max_time = max((s.get("end", 0.0) for s in segments), default=0.0)
                if max_time > 5.0:
                    rango = st.slider(
                        "Rango (segundos)",
                        min_value=0.0, max_value=max_time,
                        value=(0.0, max_time), step=1.0
                    )
                    filtered = [
                        s for s in segments
                        if s.get("end", 0.0) >= rango[0] and s.get("start", 0.0) <= rango[1]
                    ]
                    texto_a_usar = " ".join([s.get("text", "") for s in filtered]).strip()
                    preview_segments = filtered
                else:
                    texto_a_usar = " ".join([s.get("text", "") for s in segments]).strip()
                    preview_segments = segments
        else:
            preview_segments = []


        duracion_val = 60
        if red_code == "tiktok":
            duracion_val = st.select_slider(
                "Duración (segundos)",
                options=[30, 45, 60, 90, 180],
                value=60
            )

        st.markdown("<br>", unsafe_allow_html=True)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            btn_generar = st.button(
                "Generar", use_container_width=True, type="primary",
                disabled=(not bool(texto_a_usar))
            )
        with btn_col2:
            btn_variantes = st.button(
                "3 Variantes", use_container_width=True, type="secondary",
                disabled=(not bool(texto_a_usar))
            )

        topic_timestamp = None
        first_time = "00:00"
        if selected_topics_info:
            all_ts = []
            for info in selected_topics_info:
                all_ts.extend(info["timestamps"])
            if all_ts:
                topic_timestamp = ", ".join(all_ts)
                first_time = all_ts[0].split("-")[0].strip()
        elif not selected_topics_info:
            if tema_seleccionado != "[Libre]" and tema_seleccionado.startswith("[") and "]" in tema_seleccionado:
                topic_timestamp = tema_seleccionado.split("]")[0].strip("[")
                first_time = topic_timestamp.split(",")[0].split("-")[0].strip()

        # Generación
        if btn_generar and texto_a_usar:
            with st.spinner("Generando guion..."):
                try:
                    if "Video" in formato_general and topic_timestamp:
                        st.session_state["media_start_input"] = first_time
                        
                    res = generate_script(
                        texto_fuente=texto_a_usar,
                        red=red_code,
                        tema=tema_final,
                        tono=tono_code,
                        duracion=duracion_val,
                        cliente=cliente,
                        project_name=project_name,
                        topic_timestamp=topic_timestamp
                    )
                    st.session_state["guion_actual"] = res
                    st.session_state["guion_variantes"] = None
                    st.session_state["visual_slides_data"] = None  # Resetear visual
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if btn_variantes and texto_a_usar:
            with st.spinner("Generando 3 variantes..."):
                try:
                    variantes = []
                    for i in range(3):
                        var_res = generate_script(
                            texto_fuente=texto_a_usar,
                            red=red_code,
                            tema=f"{tema_final} (Enfoque {i+1})" if tema_final else f"Enfoque {i+1}",
                            tono=tono_code,
                            duracion=duracion_val,
                            cliente=cliente,
                            project_name=project_name
                        )
                        variantes.append(var_res)
                    st.session_state["guion_variantes"] = variantes
                    st.session_state["guion_actual"] = variantes[0]
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Columna Derecha: Preview
    with col_res:
        st.markdown('<p class="step-section-title">Vista previa</p>', unsafe_allow_html=True)

        guion_actual = st.session_state.get("guion_actual")
        variantes = st.session_state.get("guion_variantes")

        if variantes and len(variantes) == 3:
            tab_v1, tab_v2, tab_v3 = st.tabs(["Variante 1", "Variante 2", "Variante 3"])
            for idx, (tab_v, v_data) in enumerate(zip([tab_v1, tab_v2, tab_v3], variantes)):
                with tab_v:
                    _render_preview(v_data)
                    if st.button(
                        f"Seleccionar variante {idx+1}",
                        key=f"btn_var_{idx}",
                        use_container_width=True
                    ):
                        st.session_state["guion_actual"] = v_data
                        st.session_state["guion_variantes"] = None
                        st.session_state["visual_slides_data"] = None
                        st.rerun()

        elif guion_actual:
            _render_preview(guion_actual)
            st.markdown("---")

            st.download_button(
                label="Descargar (.md)",
                data=guion_actual.get("markdown", ""),
                file_name=f"{guion_actual.get('red', 'guion')}_{slugify(guion_actual.get('titulo', 'guion'))}_{project_name}.md",
                mime="text/markdown",
                use_container_width=True
            )

            with st.expander("Ver Markdown"):
                st.code(guion_actual.get("markdown", ""), language="markdown")

        else:
            if selected_topics_info and preview_segments:
                st.markdown("""
                <div class="exec-card" style="padding:1.5rem;">
                    <p style="font-size:0.85rem; font-weight:600; color:var(--accent); margin-bottom:0.75rem;">
                        FRAGMENTOS SELECCIONADOS
                    </p>
                """, unsafe_allow_html=True)
                
                from src.core.markdown_builder import format_timestamp
                visor = st.container(height=300)
                with visor:
                    for s in preview_segments:
                        start_ts = format_timestamp(s.get("start", 0.0))
                        st.markdown(
                            f'<div style="margin-bottom:6px; font-size:0.875rem;">'
                            f'<span class="timestamp-tag">{start_ts}</span>'
                            f'<span style="color:var(--text-secondary);">{s.get("text", "")}</span></div>',
                            unsafe_allow_html=True
                        )
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="exec-card" style="text-align:center; padding:2rem; color:#4B5563;">
                    <p style="font-size:0.9rem;">El guion aparecerá aquí.</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='margin:1.5rem 0; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav1:
            render_back_button("← Volver", prev_index=0)
        with col_nav2:
            render_next_button("Imagen →", next_index=2, disabled=not bool(guion_actual))
        with col_nav3:
            render_next_button("Video →", next_index=3, disabled=not bool(guion_actual))


def _render_preview(guion: dict):
    """Enruta al renderizador visual correspondiente."""
    red = guion.get("red", "tiktok").lower()
    data = guion.get("data", {})

    if red in ["tiktok", "reels", "shorts"]:
        render_script_tiktok(data)
    elif red in ["x", "twitter"]:
        render_script_twitter(data)
    else:
        render_script_social(data, red=red)
