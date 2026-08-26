import urllib.request
import urllib.error

def extract_text_from_url(url: str) -> str:
    """
    Extrae texto limpio (en formato Markdown) de una URL usando Jina Reader.
    """
    jina_url = f"https://r.jina.ai/{url}"
    req = urllib.request.Request(
        jina_url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        raise ValueError(f"Error al extraer texto de la URL: {e}")
