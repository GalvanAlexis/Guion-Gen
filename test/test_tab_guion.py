"""Tests unitarios y de integración para la pestaña GUION y sus componentes de renderizado."""
import pytest
from unittest.mock import patch, MagicMock
from src.ui.tab_guion import render_tab, _render_preview
from src.ui.components import (
    render_script_tiktok,
    render_script_twitter,
    render_script_social
)
from src.core.script_generator import slugify

def test_tab_guion_import():
    """Verifica que la función principal de tab_guion se importe correctamente."""
    assert callable(render_tab)

def test_slugify():
    """Verifica la generación limpia de slugs para nombres de archivo."""
    assert slugify("Déficit fiscal heredado vs superávit") == "deficit-fiscal-heredado-vs-superavit"
    assert slugify("¡Alerta roja en Chascomús! 2026") == "alerta-roja-en-chascomus-2026"

def test_render_script_tiktok(monkeypatch):
    """Verifica que render_script_tiktok ejecute sin lanzar excepciones."""
    mock_st_markdown = MagicMock()
    monkeypatch.setattr("streamlit.markdown", mock_st_markdown)

    data = {
        "titulo": "Superávit Fiscal en Chascomús",
        "duracion": 60,
        "hook_texto": "¿Sabías que eliminamos el déficit en tiempo récord?",
        "slides": [
            {"seg": "0-5s", "voz": "El déficit era enorme.", "visual": "Gráfico de barras en rojo", "efecto": "Alerta"},
            {"seg": "5-60s", "voz": "Hoy hay superávit fiscal.", "visual": "Corte a Milei", "efecto": "Música épica"}
        ],
        "cta": "Seguinos para más datos reales",
        "hashtags": ["#LLA", "#Chascomus", "#Superavit"]
    }

    render_script_tiktok(data)
    assert mock_st_markdown.called

def test_render_script_twitter(monkeypatch):
    """Verifica que render_script_twitter formatee tweets y contadores."""
    mock_st_markdown = MagicMock()
    mock_st_caption = MagicMock()
    monkeypatch.setattr("streamlit.markdown", mock_st_markdown)
    monkeypatch.setattr("streamlit.caption", mock_st_caption)

    data = {
        "titulo_hilo": "Hilo sobre el déficit fiscal",
        "total_tweets": 2,
        "gancho": "La verdad sobre las cuentas públicas.",
        "tweets": [
            {"num": 1, "texto": "El déficit heredado era del 5% del PBI.", "caracteres": 43, "enfoque": "Dato duro"},
            {"num": 2, "texto": "En 6 meses logramos superávit financiero.", "caracteres": 43, "enfoque": "Solución"}
        ],
        "cta": "RT y compartí la verdad.",
        "hashtags": ["#Milei", "#Economia"]
    }

    render_script_twitter(data)
    assert mock_st_markdown.called

def test_render_script_social(monkeypatch):
    """Verifica que render_script_social formatee slides PASC e inputs de caption."""
    mock_st_markdown = MagicMock()
    mock_st_caption = MagicMock()
    mock_st_text_area = MagicMock()
    monkeypatch.setattr("streamlit.markdown", mock_st_markdown)
    monkeypatch.setattr("streamlit.caption", mock_st_caption)
    monkeypatch.setattr("streamlit.text_area", mock_st_text_area)

    data = {
        "titulo": "De la Ruina al Superávit",
        "total_slides": 2,
        "slides": [
            {"slide_num": 1, "tipo": "problema", "titulo": "La herencia recibida", "cuerpo": "El gasto descontrolado.", "dato_destacado": "-5% PBI"},
            {"slide_num": 2, "tipo": "solucion", "titulo": "Orden fiscal", "cuerpo": "Cero emisión monetaria.", "dato_destacado": "+0.5% Superávit"}
        ],
        "copy_caption": "Datos duros que no te van a mostrar en los medios tradicionales.",
        "hashtags": ["#LLA", "#Libertad"]
    }

    render_script_social(data, red="instagram")
    assert mock_st_markdown.called

def test_render_preview_router(monkeypatch):
    """Verifica que _render_preview enrute correctamente según la plataforma."""
    mock_tiktok = MagicMock()
    mock_twitter = MagicMock()
    mock_social = MagicMock()

    monkeypatch.setattr("src.ui.tab_guion.render_script_tiktok", mock_tiktok)
    monkeypatch.setattr("src.ui.tab_guion.render_script_twitter", mock_twitter)
    monkeypatch.setattr("src.ui.tab_guion.render_script_social", mock_social)

    _render_preview({"red": "tiktok", "data": {}})
    assert mock_tiktok.called

    _render_preview({"red": "x", "data": {}})
    assert mock_twitter.called

    _render_preview({"red": "instagram", "data": {}})
    assert mock_social.called
