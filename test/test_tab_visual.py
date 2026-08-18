"""Pruebas automatizadas para la Pestaña 3 (VISUAL) de Guion-Gen."""
import pytest
from src.ui.tab_visual import (
    extract_slides_from_guion,
    _get_default_slides,
    TEMPLATE_OPTIONS,
    FORMAT_OPTIONS,
    render_tab
)

def test_extract_slides_default_when_none():
    """Verifica que se generen diapositivas por defecto cuando no hay guion."""
    slides = extract_slides_from_guion(None)
    assert isinstance(slides, list)
    assert len(slides) >= 3
    assert "titulo" in slides[0]
    assert "cuerpo" in slides[0]

def test_extract_slides_from_pasc_script():
    """Verifica la extracción de slides desde un guion PASC de Instagram."""
    mock_guion = {
        "red": "instagram",
        "titulo": "Carrusel Déficit",
        "data": {
            "titulo": "Déficit Cero",
            "slides": [
                {
                    "slide_num": 1,
                    "tipo": "gancho",
                    "titulo": "¿Sabías que el déficit era del 5%?",
                    "cuerpo": "Heredamos una situación crítica.",
                    "dato_destacado": "5% PBI",
                    "cta_texto": ""
                },
                {
                    "slide_num": 2,
                    "tipo": "problema",
                    "titulo": "Emisión sin respaldo",
                    "cuerpo": "Destruyó el poder adquisitivo.",
                    "dato_destacado": "Inflación",
                    "cta_texto": "Seguinos"
                }
            ]
        }
    }
    extracted = extract_slides_from_guion(mock_guion)
    assert len(extracted) == 2
    assert extracted[0]["titulo"] == "¿Sabías que el déficit era del 5%?"
    assert extracted[0]["dato_destacado"] == "5% PBI"
    assert extracted[0]["subtitulo"] == "GANCHO"
    assert extracted[1]["cta_texto"] == "Seguinos"

def test_extract_slides_from_tiktok_script():
    """Verifica la extracción de slides desde un guion técnico de TikTok."""
    mock_tiktok = {
        "red": "tiktok",
        "data": {
            "titulo": "Video TikTok",
            "cta": "¡Viva la libertad!",
            "slides": [
                {
                    "seg": "0-5s",
                    "voz": "Atención Chascomús",
                    "visual": "Plano frontal con bandera",
                    "efecto": "Corte rápido"
                },
                {
                    "seg": "5-15s",
                    "voz": "Se terminó la fiesta del gasto.",
                    "visual": "Gráfico de superávit",
                    "efecto": "Zoom in"
                }
            ]
        }
    }
    extracted = extract_slides_from_guion(mock_tiktok)
    assert len(extracted) == 2
    assert extracted[0]["titulo"] == "Plano frontal con bandera"
    assert extracted[0]["cuerpo"] == "Atención Chascomús"
    assert extracted[0]["subtitulo"] == "0-5s"
    assert extracted[0]["dato_destacado"] == "Corte rápido"
    assert extracted[1]["cta_texto"] == "¡Viva la libertad!"

def test_extract_slides_from_twitter_thread():
    """Verifica la extracción de slides desde un hilo de X."""
    mock_x = {
        "red": "x",
        "data": {
            "titulo_hilo": "Hilo sobre el Banco Central",
            "cta": "Fin.",
            "tweets": [
                {
                    "num": 1,
                    "texto": "1/5 ¿Por qué la inflación es siempre un fenómeno monetario?",
                    "enfoque": "Gancho"
                },
                {
                    "num": 2,
                    "texto": "2/5 Cuando se emite dinero sin demanda, cae el poder adquisitivo.",
                    "enfoque": "Desarrollo"
                }
            ]
        }
    }
    extracted = extract_slides_from_guion(mock_x)
    assert len(extracted) == 2
    assert extracted[0]["titulo"] == "Tweet #1"
    assert "fenómeno monetario" in extracted[0]["cuerpo"]
    assert extracted[0]["subtitulo"] == "Gancho"
    assert extracted[1]["cta_texto"] == "Fin."

def test_max_slides_limit():
    """Verifica el guardrail de máximo 10 slides permitidos."""
    mock_large = {
        "red": "instagram",
        "data": {
            "slides": [
                {"titulo": f"Slide {i}", "cuerpo": "Texto"} for i in range(15)
            ]
        }
    }
    extracted = extract_slides_from_guion(mock_large)
    assert len(extracted) == 10

def test_template_and_format_options():
    """Verifica que las opciones de plantillas y formatos concuerden con los módulos visuales."""
    assert "lla_dark" in TEMPLATE_OPTIONS.values()
    assert "alerta_roja" in TEMPLATE_OPTIONS.values()
    assert "estadistica" in TEMPLATE_OPTIONS.values()
    assert "4:5" in FORMAT_OPTIONS.values()
    assert "9:16" in FORMAT_OPTIONS.values()
    assert "1:1" in FORMAT_OPTIONS.values()

def test_render_tab_import():
    """Verifica que render_tab sea invocable y exportable."""
    assert callable(render_tab)
