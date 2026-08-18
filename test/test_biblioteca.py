"""Pruebas automatizadas para el Sistema de Biblioteca e Historial (ISS-016)."""
import os
import json
import shutil
import pytest
from pathlib import Path
from src.core.biblioteca import Biblioteca


@pytest.fixture
def temp_bib(tmp_path):
    """Fixture que provee una instancia de Biblioteca aislada en directorio temporal."""
    output_dir = tmp_path / "output"
    index_file = output_dir / "biblioteca.json"
    return Biblioteca(index_path=index_file, base_output_dir=output_dir)


def test_biblioteca_initialization(temp_bib):
    """Verifica la creación y formato base del archivo biblioteca.json."""
    assert temp_bib.index_path.exists()
    proyectos = temp_bib.listar()
    assert isinstance(proyectos, list)
    assert len(proyectos) == 0


def test_biblioteca_registrar_y_obtener(temp_bib):
    """Verifica el registro de un proyecto y su recuperación por ID."""
    proj = temp_bib.registrar(
        nombre="Discurso Parque Lezama",
        red="tiktok",
        tono="confrontacional",
        tema="La casta tiene miedo",
        etiquetas=["Milei", "Lezama", "LLA"],
        stats={"palabras": 1500, "duracion_audio": 420.0}
    )

    assert proj["id"] == "discurso-parque-lezama"
    assert proj["nombre"] == "Discurso Parque Lezama"
    assert "Milei" in proj["etiquetas"]
    assert proj["stats"]["palabras"] == 1500

    fetched = temp_bib.obtener("discurso-parque-lezama")
    assert fetched is not None
    assert fetched["tema"] == "La casta tiene miedo"


def test_biblioteca_buscar(temp_bib):
    """Verifica las capacidades de búsqueda por texto, etiqueta y red."""
    temp_bib.registrar(
        nombre="Economia y Superavit",
        red="twitter",
        tono="educativo",
        tema="Superavit fiscal de enero",
        etiquetas=["Economía", "Déficit Cero"]
    )
    temp_bib.registrar(
        nombre="Entrevista Streaming",
        red="tiktok",
        tono="informal",
        tema="Crecimiento y empleo",
        etiquetas=["Juventud", "Streaming"]
    )

    # Búsqueda por query
    res_query = temp_bib.buscar(query="superavit")
    assert len(res_query) == 1
    assert res_query[0]["id"] == "economia-y-superavit"

    # Búsqueda por etiqueta
    res_tag = temp_bib.buscar(etiqueta="streaming")
    assert len(res_tag) == 1
    assert res_tag[0]["id"] == "entrevista-streaming"

    # Búsqueda por red
    res_red = temp_bib.buscar(red="tiktok")
    assert len(res_red) == 1
    assert res_red[0]["id"] == "entrevista-streaming"

    # Búsqueda vacía retorna todo
    assert len(temp_bib.buscar()) == 2


def test_biblioteca_eliminar(temp_bib):
    """Verifica la eliminación de proyectos del índice y del disco."""
    p_id = "proyecto_a_borrar"
    proj_folder = temp_bib.output_dir / p_id
    proj_folder.mkdir(parents=True, exist_ok=True)
    sample_file = proj_folder / "guion.md"
    sample_file.write_text("# Guion de prueba", encoding="utf-8")

    temp_bib.registrar(nombre="Proyecto a Borrar", project_id=p_id)
    assert temp_bib.obtener(p_id) is not None

    # Borrado con archivos
    ok = temp_bib.eliminar(p_id, delete_files=True)
    assert ok is True
    assert temp_bib.obtener(p_id) is None
    assert not proj_folder.exists()


def test_biblioteca_exportar_zip(temp_bib):
    """Verifica el empaquetado de artefactos del proyecto en archivo ZIP."""
    p_id = "proyecto_export_zip"
    proj_folder = temp_bib.output_dir / p_id
    proj_folder.mkdir(parents=True, exist_ok=True)
    (proj_folder / "transcripcion.md").write_text("Texto transcrito", encoding="utf-8")
    (proj_folder / "carrusel").mkdir(exist_ok=True)
    (proj_folder / "carrusel" / "slide_01.png").write_bytes(b"dummy png bytes")

    temp_bib.registrar(nombre="Proyecto Export ZIP", project_id=p_id)
    zip_path = temp_bib.exportar_zip(p_id)

    assert Path(zip_path).exists()
    assert Path(zip_path).name == f"bundle_{p_id}.zip"
    assert Path(zip_path).stat().st_size > 0
