"""Pestaña 3: VISUAL — Generador de Carruseles e Imágenes con CSS y Gemini IA."""
import os
import streamlit as st
from pathlib import Path

from src.visual.css_renderer import render_carousel, render_slide, FORMATS
from src.visual.ai_renderer import ai_renderer
from src.config.settings import load_client_profile, OUTPUT_DIR
from src.core.script_generator import slugify
from src.ui.components import render_slide_card_preview

TEMPLATE_OPTIONS = {
    "LLA Dark (Violeta + Oro Oficial)": "lla_dark",
    "Alerta Roja (Urgente / Denuncia)": "alerta_roja",
    "Estadística (Datos y Gráficos)": "estadistica"
}

FORMAT_OPTIONS = {
    "Carrusel 4:5 (1080x1350 - Instagram)": "4:5",
    "Story / Reel 9:16 (1080x1920)": "9:16",
    "Cuadrado 1:1 (1080x1080 - Feed)": "1:1"
}

def extract_slides_from_guion(guion: dict | None) -> list[dict]:
    """Extrae y normaliza los datos de slides a partir del guion generado en Pestaña 2."""
    if not guion or not isinstance(guion, dict):
        return _get_default_slides()

    data = guion.get("data", {})
    red = guion.get("red", "instagram").lower()

    # Formato Carrusel PASC (Instagram / Facebook)
    if "slides" in data and isinstance(data["slides"], list) and data["slides"]:
        first_slide = data["slides"][0]
        if "cuerpo" in first_slide or "titulo" in first_slide:
            extracted = []
            for s in data["slides"]:
                extracted.append({
                    "titulo": s.get("titulo", ""),
                    "cuerpo": s.get("cuerpo", ""),
                    "subtitulo": s.get("subtitulo", s.get("tipo", "").upper()),
                    "dato_destacado": s.get("dato_destacado", ""),
                    "cta_texto": s.get("cta_texto", "")
                })
            return extracted[:10]
        
        elif "voz" in first_slide or "visual" in first_slide:
            extracted = []
            for s in data["slides"]:
                extracted.append({
                    "titulo": s.get("visual", "Toma Visual"),
                    "cuerpo": s.get("voz", ""),
                    "subtitulo": s.get("seg", ""),
                    "dato_destacado": s.get("efecto", ""),
                    "cta_texto": data.get("cta", "") if s == data["slides"][-1] else ""
                })
            return extracted[:10]

    # Formato Hilo X / Twitter
    if "tweets" in data and isinstance(data["tweets"], list) and data["tweets"]:
        extracted = []
        for tw in data["tweets"]:
            extracted.append({
                "titulo": f"Tweet #{tw.get('num', 1)}",
                "cuerpo": tw.get("texto", ""),
                "subtitulo": tw.get("enfoque", ""),
                "dato_destacado": "",
                "cta_texto": data.get("cta", "") if tw == data["tweets"][-1] else ""
            })
        return extracted[:10]

    return _get_default_slides()

def _get_default_slides() -> list[dict]:
    """Retorna diapositivas por defecto para inicializar la interfaz."""
    return [
        {
            "titulo": "¿Sabías esto sobre el déficit fiscal?",
            "subtitulo": "EL PROBLEMA",
            "cuerpo": "Durante décadas se financió el gasto público con emisión monetaria descontrolada.",
            "dato_destacado": "5% PBI",
            "cta_texto": ""
        },
        {
            "titulo": "La herencia recibida en números",
            "subtitulo": "LA AGITACIÓN",
            "cuerpo": "Una inflación reprimida que amenazaba con derivar en hiperinflación histórica.",
            "dato_destacado": "15.000% anual",
            "cta_texto": ""
        },
        {
            "titulo": "El camino hacia el superávit",
            "subtitulo": "LA SOLUCIÓN",
            "cuerpo": "Por primera vez en 16 años, alcanzamos superávit fiscal y financiero continuo.",
            "dato_destacado": "Déficit Cero",
            "cta_texto": ""
        },
        {
            "titulo": "La libertad no se negocia",
            "subtitulo": "CONCLUSIÓN",
            "cuerpo": "Sumate a la transformación de Chascomús y la provincia de Buenos Aires.",
            "dato_destacado": "LLA Chascomús",
            "cta_texto": "¡Seguinos para más contenido!"
        }
    ]

def render_tab():
    """Renderiza la pestaña de generación de carruseles e imágenes."""
    st.markdown("### 🖼 Generador Visual de Carruseles y Piezas Gráficas")
    st.caption("Renderiza piezas gráficas con tipografía colosal, fondos de cristal (Glassmorphism) o arte sintético generado por Gemini Imagen 3.")

    # 1. Recuperar contexto de sesión
    guion_actual = st.session_state.get("guion_actual")
    project_name = st.session_state.get("project_name", "proyecto_lla_01")
    cliente = st.session_state.get("client", load_client_profile("lla_chascomus"))

    # Cargar diapositivas en estado si no existen
    if "visual_slides_data" not in st.session_state:
        st.session_state["visual_slides_data"] = extract_slides_from_guion(guion_actual)

    slides_data = st.session_state["visual_slides_data"]

    # 2. Notificación de sincronización con Pestaña 2
    if guion_actual:
        tit_guion = guion_actual.get("data", {}).get("titulo") or guion_actual.get("titulo", "Guión Cargado")
        st.info(f"Sincronizado con el guión activo: **{tit_guion}** ({len(slides_data)} diapositivas).")

    col_config, col_preview = st.columns([1, 1])

    # 3. Columna Izquierda: Configuración y Edición de Slides
    with col_config:
        st.markdown("#### 1. Configuración de Diseño")

        modo_visual = st.radio(
            "Modo de Generación:",
            ["⚡ Modo CSS Rápido (Plantillas LLA)", "🎨 Modo IA Creativa (Gemini Imagen 3)"],
            horizontal=True
        )
        is_ai_mode = "Modo IA" in modo_visual

        if is_ai_mode:
            st.caption("Genera fondos conceptuales abstractos por IA y superpone la maquetación HTML/CSS (~20s por slide).")
        else:
            st.caption("Renderizado instantáneo ultra rápido con fondos oscuros OLED y paleta oficial LLA (~3s por slide).")

        c1, c2 = st.columns(2)
        with c1:
            plantilla_label = st.selectbox("Plantilla:", list(TEMPLATE_OPTIONS.keys()))
            plantilla_code = TEMPLATE_OPTIONS[plantilla_label]
        with c2:
            formato_label = st.selectbox("Formato:", list(FORMAT_OPTIONS.keys()))
            formato_code = FORMAT_OPTIONS[formato_label]

        st.markdown("#### 2. Edición de Diapositivas")
        st.caption("Ajusta el contenido textual antes de compilar:")

        # Guardrail: Máximo 10 slides
        if len(slides_data) > 10:
            st.warning("El carrusel supera el límite recomendado de 10 diapositivas. Se ajustará automáticamente a 10.")
            slides_data = slides_data[:10]
            st.session_state["visual_slides_data"] = slides_data

        # Formulario interactivo por slide
        for i, s in enumerate(slides_data):
            with st.expander(f"Slide #{i+1}: {s.get('titulo', 'Sin título')[:35]}...", expanded=(i == 0)):
                s["titulo"] = st.text_input(f"Título #{i+1}:", value=s.get("titulo", ""), key=f"v_tit_{i}")
                s["subtitulo"] = st.text_input(f"Subtítulo / Sección #{i+1}:", value=s.get("subtitulo", ""), key=f"v_sub_{i}")
                s["cuerpo"] = st.text_area(f"Cuerpo del texto #{i+1}:", value=s.get("cuerpo", ""), height=80, key=f"v_body_{i}")
                
                ec1, ec2 = st.columns(2)
                with ec1:
                    s["dato_destacado"] = st.text_input(f"Dato / Métrica #{i+1}:", value=s.get("dato_destacado", ""), key=f"v_stat_{i}")
                with ec2:
                    s["cta_texto"] = st.text_input(f"Llamado a la acción #{i+1}:", value=s.get("cta_texto", ""), key=f"v_cta_{i}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Botón de Renderizado
        btn_render = st.button("🖼 Compilar Carrusel Completo", use_container_width=True, type="primary")

        if btn_render:
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                processed_slides = []
                total_slides = len(slides_data)

                # Si está en modo IA, generar fondos artísticos
                if is_ai_mode:
                    status_text.text("Generando fondos artísticos conceptuales con Gemini Imagen 3...")
                    for idx, slide_item in enumerate(slides_data):
                        status_text.text(f"🎨 Generando arte para slide {idx+1}/{total_slides}...")
                        progress_bar.progress((idx + 1) / (total_slides * 2))
                        
                        slide_copy = dict(slide_item)
                        tema_prompt = slide_item.get("titulo", "Libertad y Economía")
                        bg_b64 = ai_renderer.get_background_b64(
                            tema=tema_prompt,
                            tono="confrontacional",
                            project_name=project_name,
                            formato=formato_code
                        )
                        if bg_b64:
                            slide_copy["bg_image_b64"] = bg_b64
                        processed_slides.append(slide_copy)
                else:
                    processed_slides = [dict(s) for s in slides_data]

                # Renderizado con Playwright
                status_text.text("Capturando capturas de alta resolución con Playwright...")
                progress_bar.progress(0.7)

                res_carousel = render_carousel(
                    template=plantilla_code,
                    slides_data=processed_slides,
                    proyecto=project_name,
                    formato=formato_code,
                    client=cliente
                )

                progress_bar.progress(1.0)
                status_text.empty()
                st.session_state["carrusel_actual"] = res_carousel
                st.success(f"¡Carrusel compilado con éxito! ({res_carousel.get('total_elapsed_sec', 0)}s | {total_slides} slides)")
                st.rerun()

            except Exception as err:
                status_text.empty()
                st.error(f"Error al compilar carrusel: {str(err)}")

    # 4. Columna Derecha: Vista Previa y Descarga de Resultados
    with col_preview:
        st.markdown("#### Previsualización de Carrusel")

        carrusel_actual = st.session_state.get("carrusel_actual")

        if carrusel_actual and "slides" in carrusel_actual and carrusel_actual["slides"]:
            slides_paths = carrusel_actual["slides"]
            zip_path = carrusel_actual.get("zip")
            total_time = carrusel_actual.get("total_elapsed_sec", 0)

            st.markdown(f"**Formato:** `{carrusel_actual.get('formato', '4:5')}` | **Tiempo:** `{total_time:.2f}s` | **Slides:** `{len(slides_paths)}`")

            # Botón de Descarga ZIP Global
            if zip_path and Path(zip_path).exists():
                with open(zip_path, "rb") as f_zip:
                    st.download_button(
                        label="📦 Descargar Carrusel Completo (.ZIP)",
                        data=f_zip.read(),
                        file_name=Path(zip_path).name,
                        mime="application/zip",
                        type="primary",
                        use_container_width=True
                    )

            st.markdown("---")

            # Grid de slides generados
            for idx, slide_p in enumerate(slides_paths):
                p_obj = Path(slide_p)
                if p_obj.exists():
                    st.markdown(f"**Slide #{idx+1}**")
                    st.image(str(p_obj), use_container_width=True)
                    
                    with open(p_obj, "rb") as f_img:
                        st.download_button(
                            label=f"📥 Descargar Slide {idx+1} (.PNG)",
                            data=f_img.read(),
                            file_name=p_obj.name,
                            mime="image/png",
                            key=f"dl_slide_{idx}",
                            use_container_width=True
                        )
                    st.markdown("<br>", unsafe_allow_html=True)

        else:
            st.info("Configura los slides y haz clic en 'Compilar Carrusel Completo' para ver las imágenes renderizadas aquí.")
            
            st.markdown("##### Estructura cargada actualmente:")
            for idx, s in enumerate(slides_data):
                render_slide_card_preview(
                    slide_num=idx + 1,
                    title=s.get("titulo", "Sin título"),
                    body=s.get("cuerpo", ""),
                    stat=s.get("dato_destacado", ""),
                    subtitle=s.get("subtitulo", "")
                )
