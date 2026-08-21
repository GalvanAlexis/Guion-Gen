"""Guion-Gen: Fábrica de Guiones y Procesamiento Multimedia para Redes Sociales."""
import streamlit as st
from src.ui.components import inject_custom_css, render_stepper, STEP_LABELS
from src.ui.tab_fuente import render_tab as render_fuente
from src.ui.tab_guion import render_tab as render_guion
from src.ui.tab_visual import render_tab as render_visual
from src.ui.tab_media import render_tab as render_media
from src.ui.tab_biblioteca import render_tab as render_biblioteca
from src.config.settings import load_client_profile, OUTPUT_DIR
import json

SESSION_DUMP_FILE = OUTPUT_DIR / ".temp_session.json"

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Guion-Gen",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Estilos de diseño ejecutivo ───────────────────────────────────────────────
inject_custom_css()

# ── Estado inicial de sesión ──────────────────────────────────────────────────
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    
    if SESSION_DUMP_FILE.exists():
        try:
            with open(SESSION_DUMP_FILE, "r", encoding="utf-8") as f:
                dump = json.load(f)
                for k, v in dump.items():
                    st.session_state[k] = v
        except Exception:
            pass

if "client" not in st.session_state:
    st.session_state["client"] = load_client_profile("lla_chascomus")

if "project_name" not in st.session_state:
    st.session_state["project_name"] = "conferencia_milei_01"

if "active_tab_index" not in st.session_state:
    st.session_state["active_tab_index"] = 0

# ── Calcular pasos completados para el stepper ────────────────────────────────
def get_completed_steps() -> list:
    """Determina qué pasos tienen datos válidos en session_state."""
    completed = []
    if st.session_state.get("segments") or st.session_state.get("transcription_text"):
        completed.append(0)  # FUENTE completado
    if st.session_state.get("guion_actual"):
        completed.append(1)  # GUION completado
    if st.session_state.get("carrusel_actual"):
        completed.append(2)  # VISUAL completado
    if st.session_state.get("exported_media"):
        completed.append(3)  # MEDIA completado
    return completed

# ── Stepper superior ──────────────────────────────────────────────────────────
current_index = st.session_state.get("active_tab_index", 0)
if current_index >= len(STEP_LABELS):
    current_index = 0

completed_steps = get_completed_steps()
render_stepper(current_index, completed_steps)

# ── Renderizado de la vista activa ────────────────────────────────────────────
if current_index == 0:
    render_fuente()
elif current_index == 1:
    render_guion()
elif current_index == 2:
    render_visual()
elif current_index == 3:
    render_media()
elif current_index == 4:
    render_biblioteca()

# ── Auto-persistencia de la sesión ─────────────────────────────────────────────
try:
    state_to_dump = {}
    for k, v in st.session_state.items():
        if type(v) in (str, int, float, bool, dict, list, type(None)):
            state_to_dump[k] = v
    SESSION_DUMP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_DUMP_FILE, "w", encoding="utf-8") as f:
        json.dump(state_to_dump, f, ensure_ascii=False)
except Exception:
    pass
