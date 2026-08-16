"""Tests unitarios para el generador de Markdown estructurado."""
import os
import pytest
from pathlib import Path
from src.core.markdown_builder import format_timestamp, extract_range, extract_golden_nuggets, build_markdown
from src.config.settings import OUTPUT_DIR

@pytest.fixture
def sample_segments():
    return [
        {"id": 0, "start": 0.0, "end": 4.5, "text": "Buenas noches a todos los presentes."},
        {"id": 1, "start": 4.5, "end": 12.0, "text": "El déficit fiscal que heredamos era del cinco por ciento del PBI."},
        {"id": 2, "start": 12.0, "end": 18.0, "text": "Hoy alcanzamos superávit fiscal primario y financiero."},
        {"id": 3, "start": 310.0, "end": 325.0, "text": "La libertad económica es el único camino hacia el crecimiento sostenido y el fin de la pobreza."},
    ]

def test_format_timestamp():
    assert format_timestamp(5.2) == "[00:05]"
    assert format_timestamp(75.8) == "[01:16]"
    assert format_timestamp(3665.0) == "[01:01:05]"

def test_extract_range(sample_segments):
    text = extract_range(sample_segments, 0.0, 15.0)
    assert "Buenas noches" in text
    assert "déficit fiscal" in text
    assert "libertad económica" not in text

def test_extract_golden_nuggets(sample_segments):
    nuggets = extract_golden_nuggets(sample_segments, n=2)
    assert len(nuggets) == 2
    # El segmento más largo debe ser el de libertad económica o déficit
    assert len(nuggets[0]["text"].split()) >= 10

def test_build_markdown(sample_segments):
    project_name = "test_md_build"
    md = build_markdown(
        sample_segments,
        project=project_name,
        title="Conferencia Magistral",
        engine_used="Groq (whisper-large-v3)"
    )

    # Validar estructura del texto
    assert "---" in md
    assert 'title: "Conferencia Magistral"' in md
    assert 'proyecto: "test_md_build"' in md
    assert "## Índice Rápido" in md
    assert "[00:00] Buenas noches" in md
    assert "## Transcripción Completa" in md
    assert "### Minuto 0" in md
    assert "### Minuto 5" in md

    # Validar archivo físico creado
    expected_file = OUTPUT_DIR / project_name / "transcripcion.md"
    assert expected_file.exists()
    assert expected_file.stat().st_size > 100

    # Limpieza
    if expected_file.exists():
        expected_file.unlink()
    if expected_file.parent.exists():
        try:
            expected_file.parent.rmdir()
        except OSError:
            pass
