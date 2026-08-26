import urllib.error
import pytest
from unittest.mock import patch, MagicMock
from src.core.web_scraper import extract_text_from_url

def test_extract_text_from_url_success():
    mock_html = b"# Test Markdown\nEste es un texto extraido."
    
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = mock_html
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        result = extract_text_from_url("https://example.com")
        
        assert "Test Markdown" in result
        assert "Este es un texto extraido" in result

def test_extract_text_from_url_error():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("Not found")
        
        with pytest.raises(ValueError, match="Error al extraer texto de la URL"):
            extract_text_from_url("https://invalid.com")
