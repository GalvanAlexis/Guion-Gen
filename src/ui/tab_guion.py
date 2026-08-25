"""Pestaña 2: GUION — Constructor de Guion Estructurado por Bloques."""
import streamlit as st
from src.ui.components import render_step_header, render_next_button, render_back_button
from src.config.settings import load_client_profile
from src.core.content_builder import generate_narrative_options
from src.core.prompt_assembler import assemble_prompt

# Definición de los 10 bloques narrativos
BLOQUES = [
    {"id": "gancho", "nombre": "GANCHO", "icono": "🎯", "desc": "Captar atención. Pregunta, dato fuerte, contraste o afirmación."},
    {"id": "problema", "nombre": "PROBLEMA", "icono": "⚠️", "desc": "Qué está pasando. Una sola idea central."},
    {"id": "dato_evidencia", "nombre": "DATO / EVIDENCIA", "icono": "📊", "desc": "Número, documento, comparación o hecho verificable."},
    {"id": "contexto", "nombre": "CONTEXTO", "icono": "🗺️", "desc": "Por qué ese dato importa. Antes vs. ahora."},
    {"id": "responsable", "nombre": "RESPONSABLE", "icono": "🏛️", "desc": "Qué decisión política produjo o agravó el problema."},
    {"id": "solucion", "nombre": "PROPUESTA / SOLUCIÓN", "icono": "💡", "desc": "Qué debería hacerse. Una propuesta concreta."},
    {"id": "identidad", "nombre": "IDENTIDAD POLÍTICA", "icono": "🗽", "desc": "Conectar con valores del espacio (libertad, eficiencia, responsabilidad)."},
    {"id": "cierre", "nombre": "CIERRE / FRASE MEMORABLE", "icono": "✨", "desc": "Frase corta que sintetice todo. Potencial titular."},
    {"id": "cta", "nombre": "CTA", "icono": "📣", "desc": "Llamado a la acción: compartir, comentar, guardar."},
    {"id": "fuente", "nombre": "FUENTE", "icono": "📄", "desc": "Organismo oficial, legislación o documento original."}
]

def render_tab():
    """Renderiza el paso 2 del wizard: constructor de guiones por bloques."""
    render_step_header(
        "Constructor Narrativo",
        "Estructurá el contenido en 10 bloques estratégicos antes de generar el guion final."
    )

    transcription_text = st.session_state.get("transcription_text", "")
    project_name = st.session_state.get("project_name", "proyecto_generico")
    cliente = st.session_state.get("client", load_client_profile("lla_chascomus"))

    # Inicializar estado de bloques si no existe
    if "narrative_options" not in st.session_state:
        st.session_state["narrative_options"] = {}
    if "narrative_selections" not in st.session_state:
        st.session_state["narrative_selections"] = {b["id"]: "" for b in BLOQUES}
    if "narrative_custom_text" not in st.session_state:
        st.session_state["narrative_custom_text"] = {b["id"]: "" for b in BLOQUES}
    if "narrative_prompt" not in st.session_state:
        st.session_state["narrative_prompt"] = ""

    col_izq, col_der = st.columns([1.2, 1], gap="large")

    with col_izq:
        st.markdown('<p class="step-section-title">Bloques Narrativos</p>', unsafe_allow_html=True)
        
        # Botón para generar/regenerar opciones con IA
        btn_label = "Regenerar opciones IA" if st.session_state["narrative_options"] else "✨ Generar opciones con IA"
        if st.button(btn_label, use_container_width=True, type="primary", disabled=not bool(transcription_text)):
            with st.spinner("Analizando transcripción y generando enfoques narrativos..."):
                opciones = generate_narrative_options(transcription_text, cliente)
                st.session_state["narrative_options"] = opciones
                # Resetear selecciones
                st.session_state["narrative_selections"] = {b["id"]: "" for b in BLOQUES}
                st.session_state["narrative_custom_text"] = {b["id"]: "" for b in BLOQUES}
                st.rerun()
                
        if not transcription_text:
            st.info("No hay transcripción cargada. Podes escribir el texto libremente en cada bloque.")
            
        st.markdown("<br>", unsafe_allow_html=True)

        for i, bloque in enumerate(BLOQUES):
            b_id = bloque["id"]
            seleccion_actual = st.session_state["narrative_selections"].get(b_id, "")
            opciones_ia = st.session_state["narrative_options"].get(b_id, [])
            
            is_complete = bool(seleccion_actual.strip())
            badge_class = "badge badge-ok" if is_complete else "block-badge"
            
            header_html = f"""
            <div class="narrative-block-header">
                <span>{bloque['icono']}</span>
                <span>{bloque['nombre']}</span>
                <span style="flex-grow:1"></span>
                <span class="{badge_class}">{"✓ Completo" if is_complete else str(i+1)}</span>
            </div>
            """
            
            # Usar la clase de contenedor para bordes
            container_css = "narrative-block narrative-block-complete" if is_complete else "narrative-block"
            st.markdown(f'<div class="{container_css}">', unsafe_allow_html=True)
            st.markdown(header_html, unsafe_allow_html=True)
            st.caption(bloque["desc"])
            
            with st.expander("Opciones de enfoque", expanded=not is_complete):
                radio_options = ["(Seleccionar...)"]
                if opciones_ia:
                    radio_options.extend([opt for opt in opciones_ia if opt.strip()])
                radio_options.append("📝 Escribir texto libre...")
                
                # Encontrar el índice de la selección actual
                default_idx = 0
                if seleccion_actual in radio_options:
                    default_idx = radio_options.index(seleccion_actual)
                elif st.session_state["narrative_custom_text"].get(b_id):
                    default_idx = len(radio_options) - 1 # El último (texto libre)
                
                def on_radio_change(block_id=b_id):
                    val = st.session_state[f"radio_{block_id}"]
                    if val != "(Seleccionar...)" and val != "📝 Escribir texto libre...":
                        st.session_state["narrative_selections"][block_id] = val
                    elif val == "(Seleccionar...)":
                        st.session_state["narrative_selections"][block_id] = ""

                sel = st.radio(
                    f"Opciones para {b_id}", 
                    radio_options,
                    index=default_idx,
                    label_visibility="collapsed",
                    key=f"radio_{b_id}",
                    on_change=on_radio_change
                )
                
                if sel == "📝 Escribir texto libre...":
                    def on_text_change(block_id=b_id):
                        st.session_state["narrative_selections"][block_id] = st.session_state[f"text_{block_id}"]
                        st.session_state["narrative_custom_text"][block_id] = st.session_state[f"text_{block_id}"]
                        
                    st.text_area(
                        "Texto libre", 
                        value=st.session_state["narrative_custom_text"].get(b_id, ""),
                        label_visibility="collapsed",
                        placeholder="Escribí el contenido para este bloque...",
                        key=f"text_{b_id}",
                        on_change=on_text_change
                    )
            
            st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<p class="step-section-title">Vista Previa del Prompt</p>', unsafe_allow_html=True)
        
        # Ensamblar prompt
        prompt_ensamblado = assemble_prompt(st.session_state["narrative_selections"], project_name, cliente)
        
        # Usamos st.text_area para que sea editable
        editor_key = f"narrative_prompt_editor_{st.session_state.get('prompt_version', 0)}"
        prompt_editable = st.text_area(
            "Editor Markdown",
            value=st.session_state.get("narrative_prompt", prompt_ensamblado) if st.session_state.get("narrative_prompt") else prompt_ensamblado,
            height=600,
            label_visibility="collapsed",
            key=editor_key
        )
        
        # Botón para regenerar y pisar las ediciones manuales si el usuario lo desea
        if st.button("🔄 Actualizar Prompt con cambios de la izquierda", use_container_width=True):
            st.session_state["narrative_prompt"] = prompt_ensamblado
            st.session_state["prompt_version"] = st.session_state.get("prompt_version", 0) + 1
            st.rerun()
            
        # Guardar en session state lo que el usuario editó
        if prompt_editable != st.session_state.get("narrative_prompt"):
            st.session_state["narrative_prompt"] = prompt_editable
        
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "Descargar Prompt (.txt)",
                data=prompt_ensamblado,
                file_name=f"prompt_{project_name}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
    st.markdown("<hr style='margin:1.5rem 0; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        render_back_button("← Volver a Fuente", prev_index=0)
    with col_nav2:
        render_next_button("Siguiente →", next_index=3)
