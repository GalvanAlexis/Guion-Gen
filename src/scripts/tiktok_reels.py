"""Generador de prompts especializados para guiones técnicos de TikTok, Reels y Shorts (9:16)."""
import json
from src.config.settings import load_client_profile

def get_tiktok_prompt(
    texto_fuente: str,
    tono: str = "confrontacional",
    tema: str = "",
    duracion: int = 60,
    cliente: dict = None
) -> dict:
    """
    Construye el system prompt y user prompt para guiones de video corto técnico en 2 columnas (VOZ / VISUAL).
    """
    if cliente is None:
        cliente = load_client_profile("lla_chascomus")

    nombre_cliente = cliente.get("nombre", "LLA Chascomús")
    restricciones = cliente.get("restricciones", [])
    hashtags_list = cliente.get("hashtags_fijos", {}).get("general", ["#LLA", "#Milei"])
    hashtags_json = json.dumps(list(hashtags_list), ensure_ascii=False)
    
    restricciones_str = "\n".join(f"- {r}" for r in restricciones)

    system_prompt = f"""Eres un estratega y guionista de élite especializado en contenido político audiovisual para videos verticales (TikTok, Instagram Reels, YouTube Shorts).
Trabajas para '{nombre_cliente}'. Tu objetivo es crear guiones técnicos de alto impacto, serios, directos, basados en datos y argumentos contundentes.

RESTRICCIONES EDITORIALES OBLIGATORIAS:
{restricciones_str}
- NUNCA uses emojis en los campos de texto si el tono es 'confrontacional' o 'serio'.
- Cada segundo cuenta: el gancho inicial (0 a 5 segundos) debe retener a la audiencia inmediatamente.
- Estructura el guion en bloques temporales coordinados entre la locución (VOZ) y lo que se muestra (VISUAL y EFECTOS).
- Tu respuesta DEBE ser ÚNICAMENTE un objeto JSON válido con comillas dobles según el esquema solicitado.
"""

    user_prompt = f"""Genera un guión técnico para un video vertical de {duracion} segundos.

PARÁMETROS:
- Tema principal: {tema if tema else 'Análisis y postura política basada en el discurso'}
- Tono requerido: {tono}
- Duración total: {duracion} segundos
- Hashtags recomendados: {', '.join(hashtags_list)}

TEXTO FUENTE TRANSCRIPTO:
\"\"\"
{texto_fuente.strip()}
\"\"\"

ESQUEMA JSON REQUERIDO (Usa estrictamente comillas dobles válidas en JSON):
{{
  "titulo": "Título corto y contundente del video",
  "duracion": {duracion},
  "hook_texto": "Frase de impacto de los primeros 5 segundos",
  "slides": [
    {{
      "seg": "00:00–00:05",
      "voz": "Texto exacto que se pronuncia en off o frente a cámara",
      "visual": "Indicaciones visuales: B-roll, textos destacados en pantalla, animaciones",
      "efecto": "Música sugerida, ritmo de edición, cortes rápidos o zoom"
    }},
    {{
      "seg": "00:05–00:20",
      "voz": "Desarrollo del primer dato o argumento",
      "visual": "Gráfico o recorte de video relevante",
      "efecto": "Efecto de sonido de impacto o cambio de plano"
    }}
  ],
  "hashtags": {hashtags_json},
  "cta": "Llamado a la acción final contundente"
}}
"""

    return {
        "system": system_prompt.strip(),
        "user": user_prompt.strip(),
        "duracion": duracion,
        "tono": tono,
        "red": "tiktok"
    }
