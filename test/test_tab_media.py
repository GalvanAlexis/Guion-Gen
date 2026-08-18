"""Pruebas automatizadas para la Pestaña 4 (MEDIA) de Guion-Gen."""
import pytest
from src.ui.tab_media import (
    parse_time_str,
    format_time_str,
    filter_segments_by_range,
    render_tab
)

def test_parse_time_str():
    """Verifica la conversión de distintos formatos de tiempo a segundos flotantes."""
    assert parse_time_str("00:00") == 0.0
    assert parse_time_str("01:30") == 90.0
    assert parse_time_str("02:15.5") == 135.5
    assert parse_time_str("01:00:00") == 3600.0
    assert parse_time_str("45") == 45.0
    assert parse_time_str("invalido") == 0.0
    assert parse_time_str("") == 0.0

def test_format_time_str():
    """Verifica el formateo de segundos flotantes a string MM:SS o HH:MM:SS."""
    assert format_time_str(0.0) == "00:00"
    assert format_time_str(90.0) == "01:30"
    assert format_time_str(3665.0) == "01:01:05"

def test_filter_segments_by_range():
    """Verifica el filtrado de segmentos según solapamiento con rango [start, end]."""
    mock_segments = [
        {"id": 0, "start": 0.0, "end": 10.0, "text": "Segmento inicial"},
        {"id": 1, "start": 10.0, "end": 25.0, "text": "Segmento medio"},
        {"id": 2, "start": 25.0, "end": 40.0, "text": "Segmento final"}
    ]

    # Rango que cubre solo el segundo segmento
    filtered = filter_segments_by_range(mock_segments, start_sec=12.0, end_sec=20.0)
    assert len(filtered) == 1
    assert filtered[0]["id"] == 1

    # Rango que abarca los primeros dos segmentos
    filtered_two = filter_segments_by_range(mock_segments, start_sec=5.0, end_sec=20.0)
    assert len(filtered_two) == 2
    assert filtered_two[0]["id"] == 0
    assert filtered_two[1]["id"] == 1

    # Rango fuera de límites
    assert filter_segments_by_range(mock_segments, start_sec=50.0, end_sec=60.0) == []
    assert filter_segments_by_range([], start_sec=0.0, end_sec=10.0) == []

def test_render_tab_import():
    """Verifica que la función render_tab sea callable."""
    assert callable(render_tab)
