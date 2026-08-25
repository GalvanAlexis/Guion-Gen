"""Pruebas para la Pestaña 3 (VISUAL) — nueva arquitectura Director Creativo."""
import pytest
from unittest.mock import MagicMock
from src.ui.tab_visual import render_tab, ESTILOS_VISUALES

def test_render_tab_importable():
    """Verifica que render_tab sea invocable."""
    assert callable(render_tab)

def test_estilos_visuales_estructura():
    """Verifica que los 5 estilos visuales tengan la estructura correcta."""
    assert len(ESTILOS_VISUALES) == 5
    for estilo in ESTILOS_VISUALES:
        assert "id" in estilo
        assert "nombre" in estilo
        assert "uso" in estilo
        assert "emoji" in estilo

def test_render_tab_execution(monkeypatch):
    """Verifica que render_tab ejecute sin lanzar excepciones."""
    mock_st = MagicMock()
    monkeypatch.setattr("src.ui.tab_visual.st", mock_st)
    mock_st.session_state = {"narrative_prompt": "Texto", "project_name": "Test"}
    mock_st.columns.return_value = [MagicMock(), MagicMock()]
    try:
        render_tab()
        success = True
    except Exception as e:
        success = False
        print(f"Error: {e}")
    assert success
