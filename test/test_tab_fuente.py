"""Tests de integración para la pestaña FUENTE."""
import pytest
from src.ui.tab_fuente import render_tab

def test_tab_fuente_import():
    """Verifica que tab_fuente se importe correctamente y su interfaz esté expuesta."""
    assert callable(render_tab)
