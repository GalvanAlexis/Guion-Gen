import pytest
from unittest.mock import patch, MagicMock
from src.core.content_builder import generate_narrative_options

def test_generate_narrative_options_no_text():
    res = generate_narrative_options("", {"nombre": "Test"})
    assert isinstance(res, dict)
    assert len(res.keys()) == 10
    for key in res:
        assert res[key] == []

def test_generate_narrative_options_uses_api_manager():
    with patch('src.core.content_builder.api_manager.generate_json') as mock_gen:
        mock_gen.return_value = {
            "data": {
                "gancho": ["1", "2", "3"],
                "problema": ["1", "2", "3"]
            }
        }
        res = generate_narrative_options("hola", {"nombre": "Test"})
        mock_gen.assert_called_once()
        assert len(res["gancho"]) == 3
        # Should pad missing options
        assert len(res["fuente"]) == 3
        assert res["fuente"] == ["", "", ""]
