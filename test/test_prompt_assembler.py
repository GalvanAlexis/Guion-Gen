import pytest
from src.core.prompt_assembler import assemble_prompt

def test_assemble_prompt_all_blocks():
    bloques = {
        "gancho": "A", "problema": "B", "dato_evidencia": "C", 
        "contexto": "D", "responsable": "E", "solucion": "F", 
        "identidad": "G", "cierre": "H", "cta": "I", "fuente": "J"
    }
    cliente = {"nombre": "Test Client"}
    res = assemble_prompt(bloques, "Test Proj", cliente)
    assert "Test Proj" in res
    assert "GANCHO:** A" in res
    assert "FUENTE:** J" in res
    assert "Test Client" in res

def test_assemble_prompt_partial():
    bloques = {
        "gancho": "A"
    }
    cliente = {"nombre": "Test Client"}
    res = assemble_prompt(bloques, "Test Proj", cliente)
    assert "GANCHO:** A" in res
    assert "PROBLEMA:** *(sin definir)*" in res
    assert "FUENTE:** *(sin definir)*" in res
