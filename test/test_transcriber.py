"""Tests para el motor de transcripción dual."""
import os
import subprocess
import pytest
from pathlib import Path
from src.core.transcriber import transcribe, get_engine_status
from src.config.settings import TEMP_DIR

@pytest.fixture
def sample_wav():
    """Genera un archivo WAV mono a 16kHz sintético de 2 segundos."""
    test_path = TEMP_DIR / "fixture_transcribe.wav"
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=2",
        "-ar", "16000",
        "-ac", "1",
        str(test_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    yield str(test_path)
    if test_path.exists():
        try:
            os.remove(test_path)
        except OSError:
            pass

def test_engine_status():
    """Verifica que el estado de los motores sea accesible."""
    status = get_engine_status()
    assert "groq_available" in status
    assert "local_available" in status
    assert status["local_available"] is True
    assert status["groq_available"] is True

def test_transcribe_groq(sample_wav):
    """Verifica la transcripción con Groq Whisper en modo automático."""
    res = transcribe(sample_wav, language="es", engine="auto")
    
    assert "engine_used" in res
    assert "Groq" in res["engine_used"] or "whisper" in res["engine_used"].lower()
    assert "segments" in res
    assert isinstance(res["segments"], list)
    assert res["elapsed_seconds"] > 0
    assert "total_words" in res

def test_transcribe_file_not_found():
    """Verifica que levantar FileNotFoundError cuando el archivo no existe."""
    with pytest.raises(FileNotFoundError):
        transcribe("archivo_inexistente_123.wav", engine="groq")

def test_prepare_audio_chunks_small_file(sample_wav):
    """Verifica que un archivo pequeño se optimice a MP3 sin fragmentar."""
    from src.core.transcriber import _prepare_audio_chunks_for_groq
    chunks = _prepare_audio_chunks_for_groq(sample_wav, max_chunk_duration_sec=600)
    assert len(chunks) == 1
    chunk_path, offset, is_temp = chunks[0]
    assert offset == 0.0
    assert Path(chunk_path).exists()
    # Limpieza
    if is_temp and Path(chunk_path).exists():
        Path(chunk_path).unlink(missing_ok=True)

def test_prepare_audio_chunks_large_file():
    """Verifica que un archivo largo se divida en fragmentos proporcionales con offsets correctos."""
    from src.core.transcriber import _prepare_audio_chunks_for_groq
    test_long_path = TEMP_DIR / "fixture_long_audio.wav"
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=15",
        "-ar", "16000",
        "-ac", "1",
        str(test_long_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Forzar chunking cada 5 segundos para probar la división
        chunks = _prepare_audio_chunks_for_groq(str(test_long_path), max_chunk_duration_sec=5)
        assert len(chunks) == 3
        assert chunks[0][1] == 0.0
        assert chunks[1][1] == 5.0
        assert chunks[2][1] == 10.0
        for cp, _, is_temp in chunks:
            assert Path(cp).exists()
            if is_temp:
                Path(cp).unlink(missing_ok=True)
    finally:
        test_long_path.unlink(missing_ok=True)

