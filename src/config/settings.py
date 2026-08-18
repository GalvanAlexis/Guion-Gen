"""Configuración global y constantes de Guion-Gen."""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Directorios principales
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / "src"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"
CLIENTS_DIR = BASE_DIR / "clients"
TEMPLATES_DIR = SRC_DIR / "templates"
RESOURCES_DIR = BASE_DIR / "recursos"
PUBLICATIONS_DIR = BASE_DIR / "publicaciones"

# Asegurar existencia de directorios clave
TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CLIENTS_DIR.mkdir(parents=True, exist_ok=True)
RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
PUBLICATIONS_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Modelos configurados
MODELS = {
    "gemini": {
        "text": "gemini-3.6-flash",
    },
    "groq": {
        "text": "openai/gpt-oss-120b",
        "whisper": "whisper-large-v3",
    },
    "whisper_local": {
        "default_model": os.getenv("WHISPER_FALLBACK_MODEL", "medium"),
        "device": "cpu",
        "compute_type": "int8",
    }
}

# Formatos de video e imagen soportados
MEDIA_FORMATS = {
    "carousel": {"name": "Carrusel 4:5 (Instagram)", "width": 1080, "height": 1350},
    "story": {"name": "Story/Reel 9:16 (TikTok/IG)", "width": 1080, "height": 1920},
    "square": {"name": "Cuadrado 1:1 (Post Feed)", "width": 1080, "height": 1080},
    "landscape": {"name": "Horizontal 16:9 (YouTube/X)", "width": 1920, "height": 1080},
}

def load_client_profile(client_id: str = "lla_chascomus") -> dict:
    """Carga el archivo JSON de perfil de cliente."""
    client_file = CLIENTS_DIR / f"{client_id}.json"
    if not client_file.exists():
        # Fallback genérico
        return {
            "id": client_id,
            "nombre": client_id.replace("_", " ").title(),
            "paleta": {
                "primario": "#8B5CF6",
                "secundario": "#F59E0B",
                "fondo": "#0a0a10",
                "texto": "#F8FAFC",
                "alerta": "#EF4444"
            },
            "tipografia": {"titulo": "Outfit", "cuerpo": "Inter"},
            "hashtags_fijos": {"general": ["#Contenido"]},
            "temas_frecuentes": [],
            "plantillas": {}
        }
    with open(client_file, "r", encoding="utf-8") as f:
        return json.load(f)
