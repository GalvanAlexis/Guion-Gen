"""Tests unitarios para la pestaña GUION."""
import pytest
from unittest.mock import patch, MagicMock
from src.ui.tab_guion import render_tab, BLOQUES

def test_tab_guion_import():
    """Verifica que la función principal de tab_guion se importe correctamente."""
    assert callable(render_tab)
    assert len(BLOQUES) == 10

def test_render_tab_execution(monkeypatch):
    """Verifica que render_tab ejecute sin lanzar excepciones."""
    # Mockear las funciones de st
    mock_st = MagicMock()
    monkeypatch.setattr("src.ui.tab_guion.st", mock_st)
    
    # Mockear session state
    mock_st.session_state = {
        "transcription_text": "Texto",
        "project_name": "Test"
    }
    
    # Mockear columnas
    mock_col1 = MagicMock()
    mock_col2 = MagicMock()
    mock_st.columns.return_value = [mock_col1, mock_col2]
    
    # Run the function
    try:
        render_tab()
        success = True
    except Exception as e:
        success = False
        print(f"Error: {e}")
        
    assert success
