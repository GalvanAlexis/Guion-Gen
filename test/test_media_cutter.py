"""Tests unitarios para el módulo MediaCutter (ISS-014)."""
import os
import pytest
from pathlib import Path
from src.core.media_cutter import MediaCutter, format_timestamp_srt, format_timestamp_vtt, split_into_dynamic_chunks


def test_format_timestamps():
    """Verifica la correcta conversión de segundos a formato SRT y VTT."""
    # 0 segundos
    assert format_timestamp_srt(0.0) == "00:00:00,000"
    assert format_timestamp_vtt(0.0) == "00:00:00.000"

    # 3.5 segundos
    assert format_timestamp_srt(3.5) == "00:00:03,500"
    assert format_timestamp_vtt(3.5) == "00:00:03.500"

    # 1 hora, 23 minutos, 45.678 segundos
    total_secs = 3600 + 23 * 60 + 45.678
    assert format_timestamp_srt(total_secs) == "01:23:45,678"
    assert format_timestamp_vtt(total_secs) == "01:23:45.678"


def test_to_srt_standard():
    """Verifica la generación básica de archivo SRT estándar."""
    cutter = MediaCutter()
    segments = [
        {"start": 0.0, "end": 3.5, "text": "El deficit era del cinco por ciento."},
        {"start": 3.5, "end": 7.2, "text": "Hoy estamos en superavit primario."}
    ]
    srt = cutter.to_srt(segments)
    assert "1" in srt
    assert "00:00:00,000 --> 00:00:03,500" in srt
    assert "El deficit era del cinco por ciento." in srt
    assert "2" in srt
    assert "00:00:03,500 --> 00:00:07,200" in srt
    assert "Hoy estamos en superavit primario." in srt


def test_to_vtt():
    """Verifica la generación de formato WebVTT."""
    cutter = MediaCutter()
    segments = [
        {"start": 1.2, "end": 4.8, "text": "Viva la libertad carajo."}
    ]
    vtt = cutter.to_vtt(segments)
    assert vtt.startswith("WEBVTT")
    assert "00:00:01.200 --> 00:00:04.800" in vtt
    assert "Viva la libertad carajo." in vtt


def test_dynamic_rhythm_chunks():
    """Verifica que oraciones largas se dividan en fragmentos de 3 a 5 palabras con timestamps progresivos."""
    segments = [
        {
            "start": 0.0,
            "end": 10.0,
            "text": "Hoy estamos reunidos una vez mas como cada diecisiete de agosto para conmemorar la gesta libertadora"
        }
    ]
    chunks = split_into_dynamic_chunks(segments, min_words=3, max_words=5)
    
    assert len(chunks) > 1, "Debe haber generado múltiples micro-segmentos"
    
    for c in chunks:
        words = c["text"].split()
        assert 3 <= len(words) <= 6, f"Tamaño de chunk fuera de rango: '{c['text']}'"
        assert c["start"] < c["end"], f"Timestamp inválido en chunk: {c}"

    # El primer chunk arranca en 0.0 y el último termina en 10.0
    assert chunks[0]["start"] == 0.0
    assert chunks[-1]["end"] == 10.0


def test_save_subtitles(tmp_path):
    """Verifica el guardado en disco de los formatos .srt, .vtt y .txt."""
    cutter = MediaCutter(output_dir=tmp_path)
    segments = [
        {"start": 0.0, "end": 2.5, "text": "Primera oracion de prueba."},
        {"start": 2.5, "end": 5.0, "text": "Segunda oracion de prueba con varias palabras para ver el ritmo."}
    ]
    res = cutter.save_subtitles(segments, proyecto="test_proj", nombre="test_sub", dynamic_rhythm=True)

    assert "srt" in res
    assert "vtt" in res
    assert "txt" in res
    assert os.path.exists(res["srt"])
    assert os.path.exists(res["vtt"])
    assert os.path.exists(res["txt"])

    content_srt = Path(res["srt"]).read_text(encoding="utf-8")
    assert "-->" in content_srt
