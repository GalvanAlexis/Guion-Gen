"""Tests unitarios para el módulo de configuración y perfiles de cliente."""
import pytest
from src.config.settings import load_client_profile, BASE_DIR, TEMP_DIR, OUTPUT_DIR, CLIENTS_DIR, MODELS

def test_directories_exist():
    """Verifica que las rutas base del sistema existan."""
    assert BASE_DIR.exists()
    assert TEMP_DIR.exists()
    assert OUTPUT_DIR.exists()
    assert CLIENTS_DIR.exists()

def test_load_client_profile_lla():
    """Verifica la carga del perfil oficial de LLA Chascomús."""
    profile = load_client_profile("lla_chascomus")
    assert profile["id"] == "lla_chascomus"
    assert "nombre" in profile
    assert profile["paleta"]["primario"] == "#8B5CF6"
    assert profile["paleta"]["secundario"] == "#F59E0B"
    assert len(profile["temas_frecuentes"]) >= 10
    assert "discurso_hilo" in profile["plantillas"]
    assert "estadistica_pasc" in profile["plantillas"]

def test_load_client_profile_fallback():
    """Verifica que un cliente inexistente retorne una estructura por defecto válida."""
    profile = load_client_profile("cliente_inexistente_123")
    assert profile["id"] == "cliente_inexistente_123"
    assert "paleta" in profile
    assert "primario" in profile["paleta"]

def test_models_config():
    """Verifica que la configuración de modelos tenga los defaults correctos."""
    assert MODELS["groq"]["whisper"] == "whisper-large-v3"
    assert MODELS["gemini"]["text"] == "gemini-2.0-flash"
    assert MODELS["whisper_local"]["device"] == "cpu"
