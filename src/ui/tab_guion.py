"""Pestaña 2: GUION — Fábrica de Guiones Multicanal."""
import streamlit as st
from src.core.script_generator import generate_script, slugify
from src.ui.components import (
    render_script_tiktok,
    render_script_twitter,
    render_script_social
)
from src.config.settings import load_client_profile

def render_tab():
    """Renderiza la pestaña de generación de guiones."""
    st.markdown("### 📄 Fábrica de Guiones Multicanal")
    st.caption("Transforma la transcripción en guiones técnicos para TikTok, hilos virales para X y carruseles P.A.S.C. para Instagram/Facebook.")

    # 1. Validación de Ingesta Previa
    segments = st.session_state.get("segments", [])
    transcription_text = st.session_state.get("transcription_text", "")
    project_name = st.session_state.get("project_name", "conferencia_milei_01")
    cliente = st.session_state.get("client", load_client_profile("lla_chascomus"))

    if not segments and not transcription_text:
        st.warning("No hay transcripción o contenido fuente cargado todavía.")
        c1, c2 = st.columns([1, 2])
        with c1:
            if st.button("🎙 Ir a Pestaña 1 (FUENTE)", type="primary", use_container_width=True):
                st.session_state["active_tab_index"] = 0
                st.rerun()
        with c2:
            st.info("O ingresa un texto de prueba directamente abajo para continuar.")
            direct_input = st.text_area("Texto fuente directo:", height=100, placeholder="Pega un fragmento de discurso aquí...")
            if direct_input.strip():
                transcription_text = direct_input.strip()
                st.session_state["transcription_text"] = transcription_text

    col_cfg, col_res = st.columns([1, 1])

    # 2. Columna Izquierda: Configuración
    with col_cfg:
        st.markdown("#### Configuración de Guión")
        
        red_opciones = {
            "TikTok / Reels (9:16 Video Corto)": "tiktok",
            "X / Twitter (Hilo Viral)": "x",
            "Instagram (Carrusel P.A.S.C.)": "instagram",
            "Facebook (Copy Largo / Carrusel)": "facebook"
        }
        red_label = st.selectbox("Plataforma destino:", list(red_opciones.keys()))
        red_code = red_opciones[red_label]

        tono_opciones = {
            "Confrontacional / Alerta (Político)": "confrontacional",
            "Educativo / Datos duros": "educativo",
            "Urgente / Denuncia": "urgente",
            "Motivacional": "motivacional"
        }
        tono_label = st.selectbox("Tono de comunicación:", list(tono_opciones.keys()))
        tono_code = tono_opciones[tono_label]

        # Temas sugeridos desde el perfil del cliente
        temas_sugeridos = cliente.get("temas_frecuentes", [])
        tema_seleccionado = st.selectbox(
            "Temas sugeridos de marca (LLA Chascomús):",
            ["[Personalizado / Libre]"] + temas_sugeridos
        )

        if tema_seleccionado == "[Personalizado / Libre]":
            tema_final = st.text_input("Tema específico a enfatizar:", placeholder="Ej: Déficit fiscal heredado vs superávit")
        else:
            tema_final = st.text_input("Tema específico:", value=tema_seleccionado)

        # Filtro de rango de transcripción si hay timestamps
        texto_a_usar = transcription_text
        if segments:
            max_time = max((s.get("end", 0.0) for s in segments), default=0.0)
            if max_time > 5.0:
                rango = st.slider(
                    "Rango de tiempo de la transcripción a usar (segundos):",
                    min_value=0.0,
                    max_value=max_time,
                    value=(0.0, max_time),
                    step=1.0
                )
                filtered = [
                    s.get("text", "") for s in segments 
                    if s.get("end", 0.0) >= rango[0] and s.get("start", 0.0) <= rango[1]
                ]
                texto_a_usar = " ".join(filtered).strip()
            else:
                texto_a_usar = " ".join([s.get("text", "") for s in segments]).strip()

        # Duración condicional para videos cortos
        duracion_val = 60
        if red_code == "tiktok":
            duracion_val = st.select_slider(
                "Duración estimada (segundos):",
                options=[30, 45, 60, 90, 180],
                value=60
            )

        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            btn_generar = st.button("✨ Generar Guión", use_container_width=True, type="primary", disabled=(not bool(texto_a_usar)))
        
        with btn_col2:
            btn_variantes = st.button("⚡ 3 Variantes", use_container_width=True, type="secondary", disabled=(not bool(texto_a_usar)))

        # Lógica de Ejecución Simple
        if btn_generar and texto_a_usar:
            with st.spinner("Generando guión especializado con IA..."):
                try:
                    res = generate_script(
                        texto_fuente=texto_a_usar,
                        red=red_code,
                        tema=tema_final,
                        tono=tono_code,
                        duracion=duracion_val,
                        cliente=cliente,
                        project_name=project_name
                    )
                    st.session_state["guion_actual"] = res
                    st.session_state["guion_variantes"] = None
                    st.success(f"Guión generado con éxito ({res.get('latency_seconds', 0):.2f}s | {res.get('tokens_used', 0)} tokens)")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al generar guión: {str(e)}")

        # Lógica de Ejecución 3 Variantes
        if btn_variantes and texto_a_usar:
            with st.spinner("Generando 3 variantes comparativas..."):
                try:
                    variantes = []
                    # Generar 3 variaciones
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
                    st.success("¡3 Variantes generadas exitosamente!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al generar variantes: {str(e)}")

    # 3. Columna Derecha: Vista Previa y Acciones
    with col_res:
        st.markdown("#### Vista Previa del Guión")

        guion_actual = st.session_state.get("guion_actual")
        variantes = st.session_state.get("guion_variantes")

        if variantes and len(variantes) == 3:
            st.info("Comparando 3 Variantes generadas:")
            tab_v1, tab_v2, tab_v3 = st.tabs(["Variante 1", "Variante 2", "Variante 3"])
            
            for idx, (tab_v, v_data) in enumerate(zip([tab_v1, tab_v2, tab_v3], variantes)):
                with tab_v:
                    _render_preview(v_data)
                    if st.button(f"📌 Seleccionar Variante {idx+1} como Principal", key=f"btn_var_{idx}"):
                        st.session_state["guion_actual"] = v_data
                        st.session_state["guion_variantes"] = None
                        st.rerun()

        elif guion_actual:
            _render_preview(guion_actual)

            st.markdown("---")
            # Acciones de exportación y transición
            act1, act2 = st.columns(2)
            with act1:
                st.download_button(
                    label="📥 Descargar Guion (.md)",
                    data=guion_actual.get("markdown", ""),
                    file_name=f"{guion_actual.get('red', 'guion')}_{slugify(guion_actual.get('titulo', 'guion'))}_{project_name}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with act2:
                if st.button("🖼 Enviar a Visual (Pestaña 3) →", use_container_width=True, type="primary"):
                    st.session_state["active_tab_index"] = 2
                    st.rerun()

            with st.expander("Ver Markdown Crudo"):
                st.code(guion_actual.get("markdown", ""), language="markdown")

        else:
            st.markdown("""
            <div class="glass-card">
                <p style="color: #94A3B8; font-style: italic;">Selecciona una plataforma y genera un guión para ver la estructura aquí.</p>
            </div>
            """, unsafe_allow_html=True)

def _render_preview(guion: dict):
    """Función auxiliar que enruta al renderizador visual correspondiente."""
    red = guion.get("red", "tiktok").lower()
    data = guion.get("data", {})

    if red in ["tiktok", "reels", "shorts"]:
        render_script_tiktok(data)
    elif red in ["x", "twitter"]:
        render_script_twitter(data)
    else:
        render_script_social(data, red=red)
