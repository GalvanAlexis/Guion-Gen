"""Tests unitarios e integración para el extractor y normalizador de audio."""
import os
import subprocess
import pytest
from pathlib import Path
from src.core.audio_extractor import check_ffmpeg, extract_audio_from_file, get_audio_info, extract_audio
from src.config.settings import TEMP_DIR

@pytest.fixture
def sample_audio():
    """Genera un archivo MP3 sintético de 2 segundos para testing."""
    test_path = TEMP_DIR / "fixture_test.mp3"
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=2",
        "-c:a", "libmp3lame",
        str(test_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    yield str(test_path)
    if test_path.exists():
        try:
            os.remove(test_path)
        except OSError:
            pass

def test_check_ffmpeg():
    """Verifica que FFmpeg esté correctamente detectado en el sistema."""
    assert check_ffmpeg() is True

def test_extract_audio_from_file(sample_audio):
    """Verifica la normalización a WAV 16kHz mono."""
    res = extract_audio_from_file(sample_audio)
    
    assert os.path.exists(res["path"])
    assert res["path"].endswith(".wav")
    assert res["sample_rate"] == 16000
    assert res["channels"] == 1
    assert res["duration"] > 0
    assert res["source_type"] == "file"

    # Cleanup del archivo generado
    if os.path.exists(res["path"]):
        os.remove(res["path"])

def test_get_audio_info(sample_audio):
    """Verifica la inspección determinista de ffprobe."""
    info = get_audio_info(sample_audio)
    assert info["duration"] == 2.0 or info["duration"] > 1.8
    assert "size_bytes" in info
    assert info["size_bytes"] > 0

def test_extract_audio_dispatcher(sample_audio):
    """Verifica la función unificada extract_audio con archivos locales."""
    res = extract_audio(sample_audio, project_name="test_proj")
    assert os.path.exists(res["path"])
    assert "test_proj" in res["path"]
    if os.path.exists(res["path"]):
        os.remove(res["path"])
