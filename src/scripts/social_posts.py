"""Generador de prompts especializados para carruseles P.A.S.C. y copys de Instagram y Facebook."""
import json
from src.config.settings import load_client_profile

def get_social_post_prompt(
    texto_fuente: str,
    red: str = "instagram",
    tono: str = "educativo",
    tema: str = "",
    cantidad_slides: int = 5,
    cliente: dict = None
) -> dict:
    """
    Construye el system prompt y user prompt para carruseles de Instagram/Facebook con la estructura P.A.S.C.
    (Problema -> Agitación -> Solución -> Cierre) y redacción de copys profesionales.
    """
    if cliente is None:
        cliente = load_client_profile("lla_chascomus")

    nombre_cliente = cliente.get("nombre", "LLA Chascomús")
    restricciones = cliente.get("restricciones", [])
    hashtags_list = cliente.get("hashtags_fijos", {}).get("economia" if "econom" in tema.lower() else "general", ["#LLA", "#LibertadAvanza"])
    hashtags_json = json.dumps(list(hashtags_list), ensure_ascii=False)

    restricciones_str = "\n".join(f"- {r}" for r in restricciones)

    system_prompt = f"""Eres un director creativo y copywriter de alto nivel para redes sociales (Instagram y Facebook) de '{nombre_cliente}'.
Tu objetivo es diseñar carruseles visuales de 4:5 estructurados bajo el framework P.A.S.C. (Problema, Agitación, Solución y Cierre) y redactar captions persuasivos.

REGLAS DE DISEÑO Y REDACCIÓN:
{restricciones_str}
- NUNCA uses emojis si el tono es 'confrontacional' o 'serio'.
- Cada slide debe ser sintético y visualmente escaneable: títulos potentes de 3 a 7 palabras y textos de cuerpo de máximo 3 líneas.
- No sobrecargues los slides de texto; los detalles explicativos van en el 'copy_caption'.
- Slide 1: Gancho irresistible (pregunta o dato demoledor).
- Slide 2: El problema de fondo.
- Slide 3: Agitación / Datos estadísticos y costos reales para el ciudadano.
- Slide 4: La solución basada en libertad económica y reforma institucional.
- Slide 5: Cierre con llamada a la acción clara (comentar, compartir o guardar).
- Tu respuesta DEBE ser ÚNICAMENTE un objeto JSON válido con comillas dobles según el esquema solicitado.
"""

    user_prompt = f"""Genera un carrusel de {cantidad_slides} slides y su copy caption para {red.capitalize()}.

PARÁMETROS:
- Red social: {red}
- Tema del carrusel: {tema if tema else 'Análisis y propuesta política'}
- Tono requerido: {tono}
- Cantidad de diapositivas: {cantidad_slides}
- Hashtags: {', '.join(hashtags_list)}

TEXTO FUENTE TRANSCRIPTO:
\"\"\"
{texto_fuente.strip()}
\"\"\"

ESQUEMA JSON REQUERIDO (Usa estrictamente comillas dobles válidas en JSON):
{{
  "tipo": "carousel",
  "red": "{red}",
  "titulo": "Título de portada del carrusel",
  "total_slides": {cantidad_slides},
  "slides": [
    {{
      "slide_num": 1,
      "tipo": "gancho",
      "titulo": "¿Sabías que heredamos un déficit del 5% del PBI?",
      "cuerpo": "Para ponerlo en perspectiva, equivale a imprimir billones por día.",
      "dato_destacado": "5% PBI",
      "pie": "{nombre_cliente}"
    }},
    {{
      "slide_num": 2,
      "tipo": "problema",
      "titulo": "El gasto público descontrolado",
      "cuerpo": "Durante años se financió gasto político con emisión e inflación.",
      "dato_destacado": "",
      "pie": "{nombre_cliente}"
    }}
  ],
  "copy_caption": "Texto completo del pie de foto con saltos de línea claros y hashtags incluidos al final.",
  "hashtags": {hashtags_json},
  "cta": "¿Estás de acuerdo? Dejá tu opinión en los comentarios."
}}
"""

    return {
        "system": system_prompt.strip(),
        "user": user_prompt.strip(),
        "red": red,
        "tono": tono,
        "cantidad_slides": cantidad_slides
    }
