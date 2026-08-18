"""Pruebas automatizadas para la Pestaña 5 (BIBLIOTECA) de Guion-Gen."""
import pytest
from src.ui.tab_biblioteca import (
    compute_library_metrics,
    gather_unique_tags,
    render_tab
)

def test_compute_library_metrics_empty():
    """Verifica el cálculo de métricas con lista vacía de proyectos."""
    metrics = compute_library_metrics([])
    assert metrics["total_proyectos"] == 0
    assert metrics["total_palabras"] == 0
    assert metrics["total_imagenes"] == 0
    assert metrics["total_clips"] == 0

def test_compute_library_metrics_with_data():
    """Verifica el cálculo acumulado de métricas de biblioteca."""
    mock_proyectos = [
        {
            "id": "p1",
            "stats": {"palabras": 1200},
            "archivos": {
                "carrusel": ["slide_01.png", "slide_02.png"],
                "clips": ["clip_01.mp4"]
            }
        },
        {
            "id": "p2",
            "stats": {"palabras": 3500},
            "archivos": {
                "carrusel": ["slide_01.png"],
                "clips": ["clip_01.mp4", "clip_02.mp4"]
            }
        }
    ]
    metrics = compute_library_metrics(mock_proyectos)
    assert metrics["total_proyectos"] == 2
    assert metrics["total_palabras"] == 4700
    assert metrics["total_imagenes"] == 3
    assert metrics["total_clips"] == 3

def test_gather_unique_tags():
    """Verifica la extracción y deduplicación de etiquetas únicas."""
    mock_proyectos = [
        {"etiquetas": ["Milei", "LLA", "Economía"]},
        {"etiquetas": ["Chascomús", "LLA", "Seguridad"]},
        {"etiquetas": []}
    ]
    tags = gather_unique_tags(mock_proyectos)
    assert len(tags) == 5
    assert "Chascomús" in tags
    assert "Milei" in tags
    assert "LLA" in tags

def test_render_tab_import():
    """Verifica que la función render_tab sea invocable."""
    assert callable(render_tab)
