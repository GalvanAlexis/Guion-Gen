"""Pestaña 3: VISUAL — Director Creativo y Ensamblador de Brief Visual."""
import streamlit as st
import pandas as pd
from src.ui.components import render_step_header, render_next_button, render_back_button
from src.config.settings import load_client_profile
from src.core.visual_brief import build_visual_brief
from src.core.visual_enhancer import generate_table_items, enhance_visual_prompt, COLS_IMAGEN, COLS_VIDEO

ESTILOS_VISUALES = [
    {"id": "campaign_premium", "nombre": "Campaign Premium + Editorial News", "uso": "Noticias y posicionamiento", "emoji": "📰"},
    {"id": "data_infografia", "nombre": "Data / Infografía", "uso": "Economía y estadísticas", "emoji": "📊"},
    {"id": "academico_evidence", "nombre": "Académico / Evidence", "uso": "Propuestas y políticas públicas", "emoji": "🎓"},
    {"id": "impact_breaking", "nombre": "Impact / Breaking News", "uso": "Respuesta a noticias", "emoji": "🔥"},
    {"id": "cinematografico", "nombre": "Cinematográfico", "uso": "Emoción, identidad y storytelling", "emoji": "🎬"}
]

def render_tab():
    """Renderiza el paso 3 del wizard: Director Creativo."""
    render_step_header(
        "Director Creativo",
        "Definí el estilo, formato y estructura visual para enriquecer el guion narrativo."
    )

    narrative_prompt = st.session_state.get("narrative_prompt", "")
    project_name = st.session_state.get("project_name", "proyecto_generico")
    cliente = st.session_state.get("client", load_client_profile("lla_chascomus"))
    
    if not narrative_prompt:
        st.warning("No hay un guion narrativo previo cargado. Podés continuar definiendo la estructura visual de forma independiente.")

    col_izq, col_der = st.columns([1, 1], gap="large")

    with col_izq:
        st.markdown('<p class="step-section-title">Parámetros Creativos</p>', unsafe_allow_html=True)
        
        # 1. Tipo y Red Social
        c1, c2 = st.columns(2)
        tipo_contenido = c1.selectbox("Tipo de Contenido", ["Imagen", "Video"])
        
        redes = ["Instagram", "TikTok", "X / Twitter", "Facebook", "YouTube Shorts"]
        if tipo_contenido == "Imagen":
            redes = ["Instagram", "X / Twitter", "Facebook"]
        red_social = c2.selectbox("Red Social", redes)
        
        # 2. Dimensiones
        dimensiones_opts = ["4:5 (1080x1350)", "9:16 (1080x1920)", "1:1 (1080x1080)", "16:9 (1920x1080)"]
        default_dim = 0
        if red_social in ["TikTok", "YouTube Shorts"]:
            default_dim = 1
            
        dimensiones = st.selectbox("Dimensiones", dimensiones_opts, index=default_dim)
        
        # 3. Estilo Visual
        st.markdown('<p class="step-section-title" style="margin-top:1rem;">Línea Visual</p>', unsafe_allow_html=True)
        
        estilo_opts = list(ESTILOS_VISUALES)
        estilo_opts.append({"id": "libre", "nombre": "Escribir estilo libre...", "uso": "Personalizado", "emoji": "📝"})
        
        estilo_seleccionado = st.radio(
            "Línea Visual",
            estilo_opts,
            format_func=lambda e: f"{e['emoji']} {e['nombre']} — {e['uso']}",
            label_visibility="collapsed"
        )
        
        if estilo_seleccionado["id"] == "libre":
            estilo_libre_txt = st.text_input("Ingresá tu estilo visual", placeholder="Ej: Estilo retro, paleta neón...")
            estilo_seleccionado = {"id": "libre", "nombre": estilo_libre_txt if estilo_libre_txt else "Estilo Libre", "uso": "Personalizado", "emoji": "📝"}
        
        # 4. Estructura (Data Editor)
        st.markdown('<p class="step-section-title" style="margin-top:1rem;">Estructura de Contenido</p>', unsafe_allow_html=True)
        
        df_editado = pd.DataFrame()
        
        if tipo_contenido == "Imagen":
            cant_items = st.number_input("Cantidad de láminas", min_value=1, max_value=10, value=4)
            cant_key = "cant_laminas"
            df_key = "visual_df_imagen"
            cols = COLS_IMAGEN
            empty_row = lambda i: {c: (i if c == "Nro" else f"Lámina {i}" if c == "Título" else "") for c in cols}
        else:
            cant_items = st.number_input("Cantidad de escenas", min_value=1, max_value=20, value=4)
            cant_key = "cant_escenas"
            df_key = "visual_df_video"
            cols = COLS_VIDEO
            empty_row = lambda i: {c: (i if c == "Nro" else f"Escena {i}" if c == "Descripción Visual" else 3 if c == "Duración (s)" else "") for c in cols}

        # Re-inicializar tabla si cambia cant o tipo
        if (df_key not in st.session_state or 
            len(st.session_state[df_key]) != cant_items or
            list(st.session_state[df_key].columns) != cols):
            st.session_state[df_key] = pd.DataFrame([empty_row(i) for i in range(1, cant_items + 1)])

        # Botón IA para auto-completar tabla
        if st.button("✨ Auto-completar tabla con IA", use_container_width=True, disabled=not bool(narrative_prompt)):
            with st.spinner("Generando estructura con IA..."):
                items_generados = generate_table_items(
                    narrative_prompt, tipo_contenido, cant_items, estilo_seleccionado, cliente
                )
                if items_generados:
                    # Rellenar el df con los resultados, respetando las columnas esperadas
                    rows = []
                    for i, item in enumerate(items_generados):
                        row = {c: item.get(c, empty_row(i+1).get(c, "")) for c in cols}
                        row["Nro"] = i + 1
                        rows.append(row)
                    st.session_state[df_key] = pd.DataFrame(rows)
                    st.rerun()
                else:
                    st.error("La IA no devolvió resultados. Revisá la conexión o completá la tabla manualmente.")
        
        df_editado = st.data_editor(st.session_state[df_key], use_container_width=True, hide_index=True)
        st.session_state[df_key] = df_editado
            
        # Tiempo total (solo video)
        if tipo_contenido == "Video":
            try:
                total_seg = df_editado["Duración (s)"].sum()
                st.info(f"⏱️ **Tiempo Total Estimado:** {total_seg} segundos")
            except Exception:
                pass

    with col_der:
        st.markdown('<p class="step-section-title">Brief Visual Final (.md)</p>', unsafe_allow_html=True)
        
        # Brief auto-generado desde parámetros
        brief_generado = build_visual_brief(
            narrative_prompt, tipo_contenido, red_social, dimensiones,
            estilo_seleccionado, df_editado, project_name, cliente
        )
        
        editor_key = f"visual_brief_editor_{st.session_state.get('brief_version', 0)}"
        brief_editable = st.text_area(
            "Editor Markdown",
            value=st.session_state.get("visual_brief_prompt", brief_generado),
            height=520,
            label_visibility="collapsed",
            key=editor_key
        )
        
        # Guardar edición manual
        if brief_editable != st.session_state.get("visual_brief_prompt"):
            st.session_state["visual_brief_prompt"] = brief_editable

        # Botones de acción
        b1, b2 = st.columns(2)
        
        with b1:
            if st.button("🔄 Actualizar desde izquierda", use_container_width=True):
                st.session_state["visual_brief_prompt"] = brief_generado
                st.session_state["brief_version"] = st.session_state.get("brief_version", 0) + 1
                st.rerun()
        
        with b2:
            # Filtro IA: mejora el prompt con lenguaje natural + detalles técnicos
            if st.button("🎨 Mejorar Brief con IA", use_container_width=True, type="primary"):
                with st.spinner("Aplicando filtro creativo IA..."):
                    prompt_actual = st.session_state.get("visual_brief_prompt", brief_generado)
                    prompt_mejorado = enhance_visual_prompt(
                        prompt_actual, tipo_contenido, estilo_seleccionado,
                        red_social, dimensiones, cliente
                    )
                    st.session_state["visual_brief_prompt"] = prompt_mejorado
                    st.session_state["brief_version"] = st.session_state.get("brief_version", 0) + 1
                    st.rerun()

        st.download_button(
            "Descargar Brief Visual (.md)",
            data=st.session_state.get("visual_brief_prompt", brief_generado),
            file_name=f"brief_visual_{project_name}.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("<hr style='margin:1.5rem 0; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        render_back_button("← Volver a Guion", prev_index=1)
    with col_nav2:
        render_next_button("Siguiente →", next_index=3)
