"""Compilador de plantillas Jinja2 para renderizado HTML/CSS."""
import base64
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.config.settings import TEMPLATES_DIR, BASE_DIR, load_client_profile

_jinja_env = None

def get_jinja_env() -> Environment:
    """Obtiene o inicializa el entorno global de Jinja2."""
    global _jinja_env
    if _jinja_env is None:
        _jinja_env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=False
        )
    return _jinja_env

def _encode_image_base64(image_path: str) -> str:
    """Codifica una imagen local a Base64 si el archivo existe."""
    if not image_path:
        return ""
    full_path = Path(image_path)
    if not full_path.is_absolute():
        full_path = BASE_DIR / image_path
    if full_path.exists() and full_path.is_file():
        try:
            with open(full_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            return ""
    return ""

def render_template_to_html(template: str, data: dict, client: dict = None) -> str:
    """
    Compila una plantilla Jinja2 con los datos del slide y la configuración de marca del cliente.
    
    Args:
        template: Nombre del template ('lla_dark', 'alerta_roja', 'estadistica') o ruta 'lla_dark/index.html'
        data: Diccionario con variables de contenido del slide
        client: Diccionario con perfil de marca del cliente (opcional)
        
    Returns:
        str: Documento HTML compilado listo para Playwright
    """
    env = get_jinja_env()
    
    # Normalizar ruta del template
    template_file = template
    if not template_file.endswith(".html"):
        template_file = f"{template}/index.html"
        
    tmpl = env.get_template(template_file)
    
    if client is None:
        client = load_client_profile("lla_chascomus")
        
    # Preparar logo en base64 si está configurado
    logo_path = client.get("logo", {}).get("archivo", "")
    logo_b64 = _encode_image_base64(logo_path) if logo_path else ""
    
    # Fusionar contexto
    context = {
        "client_name": client.get("nombre", "LLA Chascomús"),
        "url": client.get("website") or client.get("redes", {}).get("instagram", "@llachascomus"),
        "logo_b64": logo_b64,
        "hashtags": data.get("hashtags") or client.get("hashtags_fijos", {}).get("general", ["#LLA", "#Chascomus", "#LibertadAvanza"]),
        **data
    }
    
    return tmpl.render(**context)
