"""Tests unitarios e integración para el motor CSS Renderer y renderizado Playwright."""
import os
import zipfile
import pytest
from pathlib import Path

from src.visual.html_renderer import render_template_to_html
from src.visual.css_renderer import render_slide, render_carousel, FORMATS
from src.config.settings import OUTPUT_DIR

def test_formats_dict():
    """Verifica las dimensiones de los formatos configurados."""
    assert FORMATS["4:5"]["width"] == 1080
    assert FORMATS["4:5"]["height"] == 1350
    assert FORMATS["9:16"]["width"] == 1080
    assert FORMATS["9:16"]["height"] == 1920

def test_html_renderer_generates_valid_html():
    """Verifica que html_renderer compile correctamente con datos y branding."""
    html = render_template_to_html(
        template="lla_dark",
        data={
            "titulo": "Déficit Cero Logrado",
            "cuerpo": "Medidas económicas de fondo.",
            "dato_destacado": "0% DÉFICIT",
            "slide_num": 1,
            "total_slides": 3
        }
    )
    assert len(html) > 500
    assert "Déficit Cero Logrado" in html
    assert "Chascomus" in html

def test_render_single_slide_4_5():
    """Verifica el renderizado de un slide individual en formato 4:5."""
    out_file = OUTPUT_DIR / "test_visual" / "slide_test_4_5.png"
    if out_file.exists():
        out_file.unlink()

    res = render_slide(
        template="lla_dark",
        data={
            "titulo": "Prueba Slide 4:5",
            "subtitulo": "Test Subtitle",
            "cuerpo": "Verificación de renderizado nítido con Playwright.",
            "dato_destacado": "100% VERIFICADO",
            "slide_num": 1,
            "total_slides": 1
        },
        output_path=str(out_file),
        formato="4:5"
    )

    assert os.path.exists(res["path"])
    assert res["size_bytes"] > 50000
    assert res["elapsed_sec"] > 0

def test_render_single_slide_9_16():
    """Verifica el renderizado de un slide individual en formato vertical 9:16."""
    out_file = OUTPUT_DIR / "test_visual" / "slide_test_9_16.png"
    if out_file.exists():
        out_file.unlink()

    res = render_slide(
        template="alerta_roja",
        data={
            "titulo": "ALERTA URGENTE 9:16",
            "cuerpo": "Verificación de formato vertical para Stories y Reels.",
            "dato_destacado": "$500M",
            "slide_num": 1,
            "total_slides": 1,
            "cta_texto": "Deslizá para ver más"
        },
        output_path=str(out_file),
        formato="9:16"
    )

    assert os.path.exists(res["path"])
    assert res["size_bytes"] > 50000

def test_render_carousel_concurrent_and_zip():
    """Verifica el renderizado concurrente de un carrusel de 3 slides y empaquetado en ZIP."""
    slides = [
        {
            "tipo": "gancho",
            "titulo": "La Gran Mentira del Déficit",
            "cuerpo": "Nos dijeron que era imposible llegar a equilibrio fiscal.",
            "dato_destacado": "-5.5% PBI"
        },
        {
            "tipo": "problema",
            "titulo": "16 Años de Emisión",
            "cuerpo": "El Banco Central financió el gasto descontrolado de la política.",
            "dato_destacado": "+200% BASE"
        },
        {
            "tipo": "solucion",
            "titulo": "Superávit Financiero",
            "cuerpo": "En mayo de 2026 se consolidó el mayor superávit del siglo.",
            "dato_destacado": "+1.2% SUPERÁVIT"
        }
    ]

    res = render_carousel(
        template="estadistica",
        slides_data=slides,
        proyecto="test_carrusel_concurrent",
        formato="4:5"
    )

    assert len(res["slides"]) == 3
    for s_path in res["slides"]:
        assert os.path.exists(s_path)
        assert os.path.getsize(s_path) > 50000

    # Verificar que el ZIP existe y contiene los 3 archivos
    zip_path = Path(res["zip"])
    assert zip_path.exists()
    assert zip_path.stat().st_size > 100000

    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert len(namelist) == 3
        assert "slide_01.png" in namelist
        assert "slide_02.png" in namelist
        assert "slide_03.png" in namelist
