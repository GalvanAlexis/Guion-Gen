"""Tests unitarios para el motor de plantillas Jinja2 y plantillas CSS LLA."""
import pytest
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.config.settings import BASE_DIR

TEMPLATES_DIR = BASE_DIR / "src" / "templates"

@pytest.fixture
def jinja_env():
    """Fixture que provee el entorno Jinja2 configurado."""
    return Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

def test_templates_directory_exists():
    """Verifica que el directorio de plantillas y sus subcarpetas existan."""
    assert TEMPLATES_DIR.exists()
    assert (TEMPLATES_DIR / "base.html").exists()
    assert (TEMPLATES_DIR / "lla_dark" / "index.html").exists()
    assert (TEMPLATES_DIR / "lla_dark" / "styles.css").exists()
    assert (TEMPLATES_DIR / "alerta_roja" / "index.html").exists()
    assert (TEMPLATES_DIR / "alerta_roja" / "styles.css").exists()
    assert (TEMPLATES_DIR / "estadistica" / "index.html").exists()
    assert (TEMPLATES_DIR / "estadistica" / "styles.css").exists()

def test_render_lla_dark(jinja_env):
    """Verifica el renderizado de la plantilla lla_dark."""
    tmpl = jinja_env.get_template("lla_dark/index.html")
    html = tmpl.render(
        titulo="Déficit Cero en Tiempo Récord",
        subtitulo="Economía LLA",
        cuerpo="En solo 6 meses se logró eliminar el déficit financiero del Estado.",
        dato_destacado="0% DÉFICIT",
        slide_num=1,
        total_slides=4,
        tipo="gancho",
        cta_texto="Seguinos para más datos reales",
        hashtags=["#LLA", "#Chascomus", "#Superavit"]
    )
    assert len(html) > 500
    assert "Déficit Cero en Tiempo Récord" in html
    assert "0% DÉFICIT" in html
    assert "1 / 4" in html
    assert "GANCHO" in html
    assert "#Superavit" in html
    assert "Outfit" in html

def test_render_alerta_roja(jinja_env):
    """Verifica el renderizado de la plantilla alerta_roja."""
    tmpl = jinja_env.get_template("alerta_roja/index.html")
    html = tmpl.render(
        titulo="DENUNCIA DE GASTO EN CHASCOMÚS",
        cuerpo="Los fondos públicos municipales se destinaron a eventos sin licitación previa.",
        dato_destacado="$150M DESVIADOS",
        slide_num=2,
        total_slides=3,
        tipo="problema",
        cta_texto="¿Dónde está la transparencia?",
        hashtags=["#Alerta", "#Chascomus"]
    )
    assert len(html) > 500
    assert "DENUNCIA DE GASTO" in html
    assert "$150M DESVIADOS" in html
    assert "ALERTA POLÍTICA" in html
    assert "2 / 3" in html

def test_render_estadistica(jinja_env):
    """Verifica el renderizado de la plantilla estadistica."""
    tmpl = jinja_env.get_template("estadistica/index.html")
    html = tmpl.render(
        titulo="SUPERÁVIT PRIMARIO HISTÓRICO",
        subtitulo="RESULTADO FISCAL MAYO 2026",
        cuerpo="Primer superávit fiscal sostenido tras 16 años de déficits consecutivos.",
        dato_destacado="+1.2% PBI",
        fuente="Ministerio de Economía / INDEC",
        slide_num=3,
        total_slides=5,
        tipo="solucion",
        hashtags=["#Superavit", "#Milei"]
    )
    assert len(html) > 500
    assert "SUPERÁVIT PRIMARIO HISTÓRICO" in html
    assert "+1.2% PBI" in html
    assert "Ministerio de Economía" in html

def test_templates_responsive_height(jinja_env):
    """Verifica que el wrapper use 100vh y no alturas fijas en px que rompan Playwright."""
    for t_name in ["lla_dark/index.html", "alerta_roja/index.html", "estadistica/index.html"]:
        tmpl = jinja_env.get_template(t_name)
        html = tmpl.render(titulo="Test", cuerpo="Test body", slide_num=1, total_slides=1)
        assert "100vh" in html
        assert "Outfit" in html
        assert "Inter" in html
