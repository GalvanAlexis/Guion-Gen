"""Tests unitarios para AIRenderer, construcción de prompts, caché local y fallback."""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.visual.ai_renderer import AIRenderer, ai_renderer
from src.visual.html_renderer import render_template_to_html

def test_build_image_prompt_structure_and_guardrails():
    """Verifica que los prompts incluyan contexto temático y guardrails de seguridad."""
    renderer = AIRenderer()

    for tono in ["confrontacional", "educativo", "motivacional", "urgente"]:
        prompt = renderer.build_image_prompt(tema="inflación y déficit fiscal", tono=tono, formato="4:5")
        assert len(prompt) > 80
        assert "no human faces" in prompt.lower()
        assert "no real politicians" in prompt.lower()
        assert "no text" in prompt.lower()
        assert "4:5 vertical" in prompt.lower()

def test_generate_background_uses_disk_cache(tmp_path):
    """Verifica que si el archivo ya existe en caché, se retorne inmediatamente sin llamar APIs."""
    import hashlib
    renderer = AIRenderer(cache_dir=tmp_path)

    # Crear imagen simulada con el nombre exacto de caché
    slug_tema = "deficit-fiscal"
    prompt_hash = hashlib.sha256("deficit fiscal_confrontacional_4:5".encode("utf-8")).hexdigest()[:12]
    cached_file = tmp_path / f"bg_{slug_tema}_{prompt_hash}.png"
    cached_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 2000)

    res = renderer.generate_background(tema="deficit fiscal", tono="confrontacional", formato="4:5", use_cache=True)
    assert res == str(cached_file)

def test_generate_background_fallback_on_error(tmp_path):
    """Verifica que retorne None de forma segura si la API falla o no hay clave."""
    renderer = AIRenderer(cache_dir=tmp_path)

    with patch.dict(os.environ, {"GOOGLE_GEMINI_API_KEY": "fake_key"}, clear=False):
        with patch("google.genai.Client", side_effect=Exception("API Quota exceeded")):
            res = renderer.generate_background(tema="tema inexistente", tono="urgente", use_cache=False)
            assert res is None

def test_get_background_b64(tmp_path):
    """Verifica la codificación Base64 cuando hay imagen disponible."""
    renderer = AIRenderer(cache_dir=tmp_path)
    sample_file = tmp_path / "sample.png"
    sample_file.write_bytes(b"test_image_data")

    with patch.object(renderer, "generate_background", return_value=str(sample_file)):
        b64_str = renderer.get_background_b64(tema="tema", tono="confrontacional")
        assert len(b64_str) > 0

    with patch.object(renderer, "generate_background", return_value=None):
        b64_empty = renderer.get_background_b64(tema="tema", tono="confrontacional")
        assert b64_empty == ""

def test_template_renders_ai_background_overlay():
    """Verifica que el template inyecte la imagen en Base64 con el overlay oscuro."""
    fake_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
    html = render_template_to_html(
        template="lla_dark",
        data={
            "titulo": "Prueba Fondo IA",
            "cuerpo": "Contenido con fondo artístico detrás.",
            "bg_image_b64": fake_b64,
            "slide_num": 1,
            "total_slides": 1
        }
    )
    assert fake_b64 in html
    assert "linear-gradient(rgba(5, 5, 15, 0.85), rgba(5, 5, 15, 0.85))" in html
