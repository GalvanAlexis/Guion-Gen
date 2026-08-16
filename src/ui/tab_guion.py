"""Pestaña 2: GUION — Fábrica de Guiones Multicanal."""
import streamlit as st

def render_tab():
    """Renderiza la pestaña de generación de guiones."""
    st.markdown("### 📄 Fábrica de Guiones Multicanal")
    st.caption("Transforma la transcripción en guiones técnicos para TikTok, hilos para X y carruseles P.A.S.C. para Instagram/Facebook.")

    col_cfg, col_res = st.columns([1, 1])

    with col_cfg:
        st.markdown("#### Configuración de Guión")
        red_social = st.selectbox(
            "Plataforma destino:",
            ["TikTok / Reels (9:16 Video Corto)", "X / Twitter (Hilo Viral)", "Instagram (Carrusel P.A.S.C.)", "Facebook (Copy Largo)"]
        )

        tono = st.selectbox(
            "Tono de comunicación:",
            ["Confrontacional / Alerta (Político)", "Educativo / Datos duros", "Urgente / Denuncia", "Motivacional"]
        )

        tema = st.text_input("Tema específico a enfatizar:", placeholder="Ej: Déficit fiscal heredado vs superávit")

        duracion = st.select_slider("Duración estimada (segundos):", options=[30, 45, 60, 90, 180], value=60)

        if st.button("✨ Generar Guión Especializado", use_container_width=True, type="primary"):
            st.info("Generación de guiones activa en ISS-008 / ISS-009.")

    with col_res:
        st.markdown("#### Vista Previa del Guión")
        st.markdown("""
        <div class="glass-card">
            <p style="color: #94A3B8; font-style: italic;">Selecciona una plataforma y genera un guión para ver la estructura aquí.</p>
        </div>
        """, unsafe_allow_html=True)
