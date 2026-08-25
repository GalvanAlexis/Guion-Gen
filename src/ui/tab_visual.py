"""Pestaña 3: VISUAL — Generador de Carruseles e Imágenes."""
import streamlit as st
from pathlib import Path

from src.visual.css_renderer import render_carousel, render_slide, FORMATS
from src.visual.ai_renderer import ai_renderer
from src.config.settings import load_client_profile, OUTPUT_DIR
from src.core.script_generator import slugify
from src.ui.components import (
    render_step_header, render_next_button, render_back_button,
    render_slide_card_preview
)

TEMPLATE_OPTIONS = {
    "LLA Dark (Violeta + Oro)": "lla_dark",
    "Alerta Roja (Urgente)": "alerta_roja",
    "Estadística (Datos)": "estadistica"
}

FORMAT_OPTIONS = {
    "Carrusel 4:5 — 1080×1350 (Instagram)": "4:5",
    "Story / Reel 9:16 — 1080×1920": "9:16",
    "Cuadrado 1:1 — 1080×1080": "1:1"
}


def extract_slides_from_guion(guion: dict | None) -> list[dict]:
    """Extrae y normaliza los datos de slides a partir del guion generado."""
    if not guion or not isinstance(guion, dict):
        return _get_default_slides()

    data = guion.get("data", {})

    if "slides" in data and isinstance(data["slides"], list) and data["slides"]:
        first_slide = data["slides"][0]
        if "cuerpo" in first_slide or "titulo" in first_slide:
            return [{
                "titulo": s.get("titulo", ""),
                "cuerpo": s.get("cuerpo", ""),
                "subtitulo": s.get("subtitulo", s.get("tipo", "").upper()),
                "dato_destacado": s.get("dato_destacado", ""),
                "cta_texto": s.get("cta_texto", "")
            } for s in data["slides"]][:10]

        elif "voz" in first_slide or "visual" in first_slide:
            return [{
                "titulo": s.get("visual", "Toma Visual"),
                "cuerpo": s.get("voz", ""),
                "subtitulo": s.get("seg", ""),
                "dato_destacado": s.get("efecto", ""),
                "cta_texto": data.get("cta", "") if s == data["slides"][-1] else ""
            } for s in data["slides"]][:10]

    if "tweets" in data and isinstance(data["tweets"], list) and data["tweets"]:
        return [{
            "titulo": f"Tweet #{tw.get('num', 1)}",
            "cuerpo": tw.get("texto", ""),
            "subtitulo": tw.get("enfoque", ""),
            "dato_destacado": "",
            "cta_texto": data.get("cta", "") if tw == data["tweets"][-1] else ""
        } for tw in data["tweets"]][:10]

    return _get_default_slides()


def _get_default_slides() -> list[dict]:
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
            "cta_texto": "¡Seguinos!"
        }
    ]


def render_tab():
    """Renderiza el paso 3 del wizard: generación de carruseles."""
    render_step_header(
        "Compilá el carrusel",
        "Ajustá el diseño, editá el texto de cada slide y compilá las imágenes."
    )

    guion_actual = st.session_state.get("guion_actual")
    project_name = st.session_state.get("project_name", "proyecto_lla_01")
    cliente = st.session_state.get("client", load_client_profile("lla_chascomus"))

    if "visual_slides_data" not in st.session_state or st.session_state["visual_slides_data"] is None:
        st.session_state["visual_slides_data"] = extract_slides_from_guion(guion_actual)

    slides_data = st.session_state["visual_slides_data"]

    if guion_actual:
        tit_guion = guion_actual.get("data", {}).get("titulo") or "Guión activo"
        st.info(f"Sincronizado con: **{tit_guion}** — {len(slides_data)} slides")

    col_config, col_preview = st.columns([1, 1], gap="large")

    # ── Configuración ─────────────────────────────────────────────────────────
    with col_config:
        st.markdown('<p class="step-section-title">Modo de generación</p>', unsafe_allow_html=True)
        modo_visual = st.radio(
            "modo",
            ["CSS Rápido (Plantillas LLA)", "IA Creativa (Gemini Imagen 3)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        is_ai_mode = "IA" in modo_visual

        if is_ai_mode:
            st.caption("Fondos generados por IA. Aprox. 20s por slide.")
        else:
            st.caption("Renderizado instantáneo con fondos OLED oscuros. Aprox. 3s por slide.")

        c1, c2 = st.columns(2)
        with c1:
            plantilla_label = st.selectbox("Plantilla", list(TEMPLATE_OPTIONS.keys()),
                                            label_visibility="collapsed")
            plantilla_code = TEMPLATE_OPTIONS[plantilla_label]
        with c2:
            formato_label = st.selectbox("Formato", list(FORMAT_OPTIONS.keys()),
                                          label_visibility="collapsed")
            formato_code = FORMAT_OPTIONS[formato_label]

        st.markdown("---")
        st.markdown('<p class="step-section-title">Contenido de slides</p>', unsafe_allow_html=True)

        if len(slides_data) > 10:
            st.warning("Máximo 10 slides. Se ajustará automáticamente.")
            slides_data = slides_data[:10]
            st.session_state["visual_slides_data"] = slides_data

        for i, s in enumerate(slides_data):
            with st.expander(f"Slide {i+1} — {s.get('titulo', '')[:35]}", expanded=(i == 0)):
                s["titulo"] = st.text_input(f"Título", value=s.get("titulo", ""),
                                             key=f"v_tit_{i}")
                s["subtitulo"] = st.text_input(f"Sección", value=s.get("subtitulo", ""),
                                                key=f"v_sub_{i}")
                s["cuerpo"] = st.text_area(f"Cuerpo", value=s.get("cuerpo", ""),
                                            height=70, key=f"v_body_{i}")
                ec1, ec2 = st.columns(2)
                with ec1:
                    s["dato_destacado"] = st.text_input("Dato / Métrica",
                                                         value=s.get("dato_destacado", ""),
                                                         key=f"v_stat_{i}")
                with ec2:
                    s["cta_texto"] = st.text_input("CTA",
                                                    value=s.get("cta_texto", ""),
                                                    key=f"v_cta_{i}")

        st.markdown("<br>", unsafe_allow_html=True)
        btn_render = st.button("Compilar carrusel", use_container_width=True, type="primary")

        if btn_render:
            progress_bar = st.progress(0)
            status_text = st.empty()
            try:
                processed_slides = []
                total_slides = len(slides_data)

                if is_ai_mode:
                    for idx, slide_item in enumerate(slides_data):
                        status_text.text(f"Generando arte para slide {idx+1}/{total_slides}...")
                        progress_bar.progress((idx + 1) / (total_slides * 2))
                        slide_copy = dict(slide_item)
                        bg_b64 = ai_renderer.get_background_b64(
                            tema=slide_item.get("titulo", "Libertad y Economía"),
                            tono="confrontacional",
                            project_name=project_name,
                            formato=formato_code
                        )
                        if bg_b64:
                            slide_copy["bg_image_b64"] = bg_b64
                        else:
                            st.toast(f"⚠️ Slide {idx+1}: Sin acceso a Gemini Imagen (Cuota/404). Usando fondo CSS.", icon="⚠️")
                        processed_slides.append(slide_copy)
                else:
                    processed_slides = [dict(s) for s in slides_data]

                status_text.text("Capturando imágenes con Playwright...")
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
                st.rerun()

            except Exception as err:
                status_text.empty()
                st.error(f"Error: {str(err)}")

    # ── Preview ───────────────────────────────────────────────────────────────
    with col_preview:
        st.markdown('<p class="step-section-title">Resultado</p>', unsafe_allow_html=True)
        carrusel_actual = st.session_state.get("carrusel_actual")

        if carrusel_actual and "slides" in carrusel_actual and carrusel_actual["slides"]:
            slides_paths = carrusel_actual["slides"]
            zip_path = carrusel_actual.get("zip")
            total_time = carrusel_actual.get("total_elapsed_sec", 0)

            st.caption(f"`{carrusel_actual.get('formato', '4:5')}` · {total_time:.1f}s · {len(slides_paths)} slides")

            if zip_path and Path(zip_path).exists():
                with open(zip_path, "rb") as f_zip:
                    st.download_button(
                        label="Descargar carrusel (.ZIP)",
                        data=f_zip.read(),
                        file_name=Path(zip_path).name,
                        mime="application/zip",
                        type="primary",
                        use_container_width=True
                    )

            st.markdown("---")

            for idx, slide_p in enumerate(slides_paths):
                p_obj = Path(slide_p)
                if p_obj.exists():
                    st.caption(f"Slide {idx+1}")
                    st.image(str(p_obj), use_container_width=True)
                    with open(p_obj, "rb") as f_img:
                        st.download_button(
                            label=f"Descargar slide {idx+1}",
                            data=f_img.read(),
                            file_name=p_obj.name,
                            mime="image/png",
                            key=f"dl_slide_{idx}",
                            use_container_width=True
                        )
                    st.markdown("<br>", unsafe_allow_html=True)

        else:
            st.markdown('<p style="color:#4B5563; font-size:0.875rem;">Compilá el carrusel para ver las imágenes aquí.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-section-title" style="margin-top:1rem;">Estructura actual</p>', unsafe_allow_html=True)
            for idx, s in enumerate(slides_data):
                render_slide_card_preview(
                    slide_num=idx + 1,
                    title=s.get("titulo", ""),
                    body=s.get("cuerpo", ""),
                    stat=s.get("dato_destacado", ""),
                    subtitle=s.get("subtitulo", "")
                )

        st.markdown("<hr style='margin:1.5rem 0; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        col_nav1, col_nav2 = st.columns([1, 1])
        with col_nav1:
            render_back_button("← Volver", prev_index=1)
        with col_nav2:
            render_next_button("Siguiente →", next_index=3)
