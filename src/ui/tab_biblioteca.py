"""Pestaña 5: BIBLIOTECA — Panel Ejecutivo de Historial y Gestión de Proyectos."""
import os
from pathlib import Path
from datetime import datetime
import streamlit as st

from src.core.biblioteca import biblioteca, Biblioteca
from src.config.settings import OUTPUT_DIR


def compute_library_metrics(proyectos: list[dict]) -> dict:
    """Calcula las métricas cuantitativas acumuladas de la biblioteca."""
    if not proyectos:
        return {
            "total_proyectos": 0,
            "total_palabras": 0,
            "total_imagenes": 0,
            "total_clips": 0
        }
    
    total_palabras = sum(p.get("stats", {}).get("palabras", 0) for p in proyectos)
    total_imagenes = sum(len(p.get("archivos", {}).get("carrusel", [])) for p in proyectos)
    total_clips = sum(len(p.get("archivos", {}).get("clips", [])) for p in proyectos)

    return {
        "total_proyectos": len(proyectos),
        "total_palabras": total_palabras,
        "total_imagenes": total_imagenes,
        "total_clips": total_clips
    }


def gather_unique_tags(proyectos: list[dict]) -> list[str]:
    """Extrae la lista ordenada de etiquetas únicas de todos los proyectos."""
    tags = set()
    for p in proyectos:
        for t in p.get("etiquetas", []):
            if t:
                tags.add(t.strip())
    return sorted(list(tags))


def render_tab():
    """Renderiza la pestaña interactiva de biblioteca y gestión de proyectos."""
    st.markdown("### 📚 Biblioteca Central de Proyectos e Historial")
    st.caption("Consulta el archivo histórico de conferencias transcriptas, guiones ejecutivos, piezas gráficas y clips exportados.")

    # 1. Cargar proyectos
    proyectos = biblioteca.listar()

    # 2. Métricas Consolidadas (KPIs)
    metrics = compute_library_metrics(proyectos)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Proyectos", metrics["total_proyectos"])
    with m2:
        st.metric("Palabras Transcritas", f"{metrics['total_palabras']:,}")
    with m3:
        st.metric("Imágenes Generadas", metrics["total_imagenes"])
    with m4:
        st.metric("Clips y Videos", metrics["total_clips"])

    st.markdown("---")

    # 3. Barra de Búsqueda y Filtrado
    st.markdown("#### 🔍 Explorador y Filtros")
    col_q, col_red, col_tag, col_sort = st.columns([2, 1, 1, 1])

    with col_q:
        search_query = st.text_input("Búsqueda libre:", placeholder="Buscar por nombre, tema o palabra clave...", key="bib_search_input")

    with col_red:
        red_filter = st.selectbox("Plataforma:", ["Todas", "TikTok", "X", "Instagram", "Facebook", "General"], key="bib_red_filter")

    unique_tags = gather_unique_tags(proyectos)
    with col_tag:
        tag_filter = st.selectbox("Etiqueta:", ["Todas"] + unique_tags, key="bib_tag_filter")

    with col_sort:
        sort_order = st.selectbox("Orden:", ["Más recientes", "Más antiguos", "Nombre (A-Z)"], key="bib_sort_order")

    # Aplicar filtros
    red_param = "" if red_filter == "Todas" else red_filter.lower()
    tag_param = "" if tag_filter == "Todas" else tag_filter
    
    filtered_projs = biblioteca.buscar(query=search_query, etiqueta=tag_param, red=red_param)

    # Ordenar resultados
    if sort_order == "Más recientes":
        filtered_projs.sort(key=lambda x: x.get("fecha", ""), reverse=True)
    elif sort_order == "Más antiguos":
        filtered_projs.sort(key=lambda x: x.get("fecha", ""), reverse=False)
    elif sort_order == "Nombre (A-Z)":
        filtered_projs.sort(key=lambda x: x.get("nombre", "").lower(), reverse=False)

    st.markdown(f"**Resultados encontrados:** `{len(filtered_projs)}` de `{len(proyectos)}` proyectos")

    # 4. Vista de Proyectos Expandibles
    if not filtered_projs:
        st.info("No se encontraron proyectos con los criterios de búsqueda seleccionados.")
    else:
        for idx, p in enumerate(filtered_projs):
            p_id = p["id"]
            p_nombre = p.get("nombre", "Proyecto sin nombre")
            p_fecha = p.get("fecha", "")[:10]
            p_red = p.get("red", "general").upper()
            p_tono = p.get("tono", "general").capitalize()
            p_tema = p.get("tema", "Sin tema especificado")
            p_tags = p.get("etiquetas", [])
            p_archivos = p.get("archivos", {})
            p_stats = p.get("stats", {})

            # Encabezado del Expander
            exp_label = f"📁 [{p_red}] {p_nombre} — {p_fecha} ({p_stats.get('palabras', 0)} palabras)"

            with st.expander(exp_label, expanded=(idx == 0 and len(filtered_projs) == 1)):
                st.markdown(f"**Tema:** *{p_tema}* | **Tono:** `{p_tono}` | **Fecha creación:** `{p_fecha}`")
                
                # Tags visuales
                if p_tags:
                    tags_html = " ".join([f'<span class="badge" style="background: rgba(139,92,246,0.15); color: #8B5CF6; margin-right: 4px;">#{t}</span>' for t in p_tags])
                    st.markdown(f'<div style="margin-bottom: 12px;">{tags_html}</div>', unsafe_allow_html=True)

                # Pestañas de Artefactos Internos
                tab_docs, tab_visual, tab_media = st.tabs(["📄 Guiones y Texto", "🖼 Piezas Gráficas", "🎬 Clips y Subtítulos"])

                # Pestaña 1: Docs & Guiones
                with tab_docs:
                    trans_file = p_archivos.get("transcripcion")
                    guion_files = p_archivos.get("guiones", [])

                    if trans_file:
                        full_trans = OUTPUT_DIR / trans_file
                        if full_trans.exists():
                            st.markdown(f"**Transcripción Base:** `{full_trans.name}`")
                            with open(full_trans, "rb") as f_tr:
                                st.download_button(
                                    label="📥 Descargar Transcripción (.md)",
                                    data=f_tr.read(),
                                    file_name=full_trans.name,
                                    mime="text/markdown",
                                    key=f"dl_tr_{p_id}_{idx}"
                                )

                    if guion_files:
                        st.markdown(f"**Guiones Generados ({len(guion_files)}):**")
                        for g_rel in guion_files:
                            full_g = OUTPUT_DIR / g_rel
                            if full_g.exists():
                                g_col1, g_col2 = st.columns([3, 1])
                                with g_col1:
                                    st.markdown(f"- `{full_g.name}`")
                                with g_col2:
                                    with open(full_g, "rb") as f_g:
                                        st.download_button(
                                            label="📥 Descargar",
                                            data=f_g.read(),
                                            file_name=full_g.name,
                                            mime="text/markdown",
                                            key=f"dl_g_{p_id}_{full_g.stem}"
                                        )
                    if not trans_file and not guion_files:
                        st.caption("No hay documentos de texto registrados en este proyecto.")

                # Pestaña 2: Visual
                with tab_visual:
                    carrusel_files = p_archivos.get("carrusel", [])
                    if carrusel_files:
                        st.markdown(f"**Imágenes del Carrusel ({len(carrusel_files)}):**")
                        cols_img = st.columns(min(4, len(carrusel_files)))
                        for img_idx, img_rel in enumerate(carrusel_files):
                            full_img = OUTPUT_DIR / img_rel
                            if full_img.exists():
                                with cols_img[img_idx % len(cols_img)]:
                                    st.image(str(full_img), use_container_width=True)
                                    with open(full_img, "rb") as f_img:
                                        st.download_button(
                                            label=f"↓ Slide {img_idx+1}",
                                            data=f_img.read(),
                                            file_name=full_img.name,
                                            mime="image/png",
                                            key=f"dl_img_{p_id}_{img_idx}"
                                        )
                    else:
                        st.caption("No hay imágenes de carrusel generadas para este proyecto.")

                # Pestaña 3: Media
                with tab_media:
                    clip_files = p_archivos.get("clips", [])
                    sub_files = p_archivos.get("subtitulos", [])

                    if clip_files:
                        st.markdown(f"**Clips de Video ({len(clip_files)}):**")
                        for clip_rel in clip_files:
                            full_clip = OUTPUT_DIR / clip_rel
                            if full_clip.exists():
                                st.video(str(full_clip))
                                with open(full_clip, "rb") as f_clip:
                                    st.download_button(
                                        label=f"📥 Descargar {full_clip.name}",
                                        data=f_clip.read(),
                                        file_name=full_clip.name,
                                        mime="video/mp4",
                                        key=f"dl_clip_{p_id}_{full_clip.stem}"
                                    )

                    if sub_files:
                        st.markdown(f"**Subtítulos Sincronizados ({len(sub_files)}):**")
                        for sub_rel in sub_files:
                            full_sub = OUTPUT_DIR / sub_rel
                            if full_sub.exists():
                                with open(full_sub, "rb") as f_sub:
                                    st.download_button(
                                        label=f"📝 Descargar {full_sub.name}",
                                        data=f_sub.read(),
                                        file_name=full_sub.name,
                                        mime="text/plain",
                                        key=f"dl_sub_{p_id}_{full_sub.stem}"
                                    )

                    if not clip_files and not sub_files:
                        st.caption("No hay clips multimedia ni subtítulos para este proyecto.")

                st.markdown("---")

                # Acciones de Proyecto (Cargar, Exportar ZIP, Eliminar)
                act_c1, act_c2, act_c3 = st.columns([1, 1, 1])

                with act_c1:
                    if st.button("🔄 Cargar en Sesión Activa", key=f"btn_load_{p_id}", use_container_width=True):
                        st.session_state["project_name"] = p_id
                        # Intentar leer transcripción si existe
                        trans_path = p_archivos.get("transcripcion")
                        if trans_path and (OUTPUT_DIR / trans_path).exists():
                            st.session_state["markdown_content"] = (OUTPUT_DIR / trans_path).read_text(encoding="utf-8")
                        st.success(f"Proyecto '{p_nombre}' cargado en la sesión activa.")
                        st.rerun()

                with act_c2:
                    try:
                        zip_file_path = biblioteca.exportar_zip(p_id)
                        with open(zip_file_path, "rb") as f_bundle:
                            st.download_button(
                                label="📦 Descargar Bundle ZIP",
                                data=f_bundle.read(),
                                file_name=f"bundle_{p_id}.zip",
                                mime="application/zip",
                                key=f"dl_zip_{p_id}",
                                use_container_width=True,
                                type="primary"
                            )
                    except Exception:
                        st.button("📦 Bundle ZIP no disponible", disabled=True, key=f"zip_na_{p_id}", use_container_width=True)

                with act_c3:
                    with st.popover("🗑️ Eliminar Proyecto"):
                        st.warning(f"¿Estás seguro de eliminar el proyecto '{p_nombre}'?")
                        del_files = st.checkbox("Eliminar también los archivos físicos de disco", value=False, key=f"chk_del_{p_id}")
                        if st.button("Confirmar Eliminación", type="primary", key=f"btn_del_conf_{p_id}"):
                            biblioteca.eliminar(p_id, delete_files=del_files)
                            st.success(f"Proyecto '{p_nombre}' eliminado con éxito.")
                            st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)
