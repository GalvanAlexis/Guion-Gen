"""Tests unitarios y de integración para APIManager."""
import pytest
from src.config.api_manager import APIManager

def test_api_manager_status():
    """Verifica que el estado de los proveedores sea consultable."""
    mgr = APIManager()
    status = mgr.get_status()
    assert "groq" in status
    assert "gemini" in status
    assert "active_provider" in status
    assert status["groq"]["available"] is True

def test_api_manager_generate_text():
    """Verifica la generación de texto a través del proveedor activo."""
    mgr = APIManager()
    res = mgr.generate(
        prompt="Responde exactamente con la palabra OK.",
        temperature=0.1,
        max_tokens=20
    )
    assert "text" in res
    assert "provider" in res
    assert "tokens_used" in res
    assert "latency_seconds" in res
    assert res["tokens_used"] > 0
    assert "OK" in res["text"].upper()

def test_api_manager_generate_json():
    """Verifica la generación y parseo determinista de JSON estructurado."""
    mgr = APIManager()
    prompt = 'Genera un JSON con los campos "titulo" (string) y "cantidad" (número).'
    res = mgr.generate_json(prompt=prompt)
    
    assert "data" in res
    assert isinstance(res["data"], dict)
    assert "titulo" in res["data"]
    assert "cantidad" in res["data"]
