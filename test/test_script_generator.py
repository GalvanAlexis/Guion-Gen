"""Tests unitarios y de integración para el orquestador Script Generator."""
import os
import pytest
from pathlib import Path
from src.core.script_generator import slugify, format_script_to_markdown, generate_script
from src.config.settings import PUBLICATIONS_DIR

SAMPLE_SOURCE = (
    "El déficit fiscal que heredamos era del cinco por ciento del PBI. "
    "Hoy alcanzamos superávit fiscal primario y financiero sin precedentes."
)

def test_slugify():
    """Verifica que la función slugify genere identificadores limpios."""
    assert slugify("Déficit vs Superávit") == "deficit-vs-superavit"
    assert slugify("¡Gran discurso en Chascomús 2026!") == "gran-discurso-en-chascomus-2026"

def test_format_script_to_markdown():
    """Verifica la conversión a Markdown para cada tipo de red."""
    tiktok_data = {
        "titulo": "Fin del Déficit",
        "duracion": 30,
        "hook_texto": "¿Sabías que eliminamos el déficit?",
        "slides": [
            {"seg": "00:00–00:05", "voz": "Texto voz", "visual": "Visual B-Roll", "efecto": "Efecto rápido"}
        ],
        "hashtags": ["#LLA", "#Milei"],
        "cta": "Seguinos para más datos"
    }
    md_tiktok = format_script_to_markdown(tiktok_data, red="tiktok")
    assert "Guion Técnico" in md_tiktok
    assert "00:00–00:05" in md_tiktok

    x_data = {
        "titulo_hilo": "Radiografía del Gasto Público",
        "gancho": "El déficit fiscal llegó a su fin [1/2]",
        "total_tweets": 2,
        "tweets": [
            {"num": 1, "texto": "Tweet 1 [1/2]", "caracteres": 15, "enfoque": "gancho"},
            {"num": 2, "texto": "Tweet 2 [2/2]", "caracteres": 15, "enfoque": "cierre"}
        ],
        "hashtags": ["#LLA"],
        "cta": "RT y debate"
    }
    md_x = format_script_to_markdown(x_data, red="x")
    assert "Hilo para X" in md_x
    assert "Tweet 1/2" in md_x

    ig_data = {
        "titulo": "Las 3 Claves del Déficit Cero",
        "total_slides": 2,
        "slides": [
            {
                "slide_num": 1,
                "tipo": "gancho",
                "titulo": "¿Déficit Cero en 12 Meses?",
                "cuerpo": "Un logro sin precedentes.",
                "dato_destacado": "5% PBI",
                "pie": "LLA Chascomús"
            },
            {
                "slide_num": 2,
                "tipo": "cierre",
                "titulo": "La Libertad Avanza",
                "cuerpo": "Sumate al cambio.",
                "dato_destacado": "",
                "pie": "LLA Chascomús"
            }
        ],
        "copy_caption": "Texto del post con detalles y fundamentos.",
        "hashtags": ["#LLA", "#Chascomus"]
    }
    md_ig = format_script_to_markdown(ig_data, red="instagram")
    assert "Carrusel para INSTAGRAM" in md_ig
    assert "Slide 1 — [GANCHO]" in md_ig
    assert "Copy Caption para la Publicación" in md_ig

def test_generate_script_invalid_network():
    """Verifica que se levante ValueError ante redes no soportadas."""
    with pytest.raises(ValueError):
        generate_script(
            texto_fuente=SAMPLE_SOURCE,
            red="red_desconocida_xyz",
            project_name="test"
        )

def test_generate_script_tiktok():
    """Verifica la generación completa y guardado de un guion de TikTok."""
    res = generate_script(
        texto_fuente=SAMPLE_SOURCE,
        red="tiktok",
        tema="Superávit fiscal",
        duracion=30,
        project_name="test_proj_scripts"
    )

    assert "red" in res
    assert res["red"] == "tiktok"
    assert "markdown" in res
    assert "json_path" in res
    assert os.path.exists(res["json_path"])
    assert os.path.exists(res["md_path"])

    # Cleanup de archivos generados durante el test
    if os.path.exists(res["json_path"]):
        os.remove(res["json_path"])
    if os.path.exists(res["md_path"]):
        os.remove(res["md_path"])
