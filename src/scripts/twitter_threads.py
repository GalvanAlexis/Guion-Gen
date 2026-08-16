"""Generador de prompts especializados para hilos virales y posts en X (Twitter)."""
import json
from src.config.settings import load_client_profile

def get_twitter_prompt(
    texto_fuente: str,
    tono: str = "confrontacional",
    tema: str = "",
    cliente: dict = None,
    cantidad_tweets: int = 7
) -> dict:
    """
    Construye el system prompt y user prompt para hilos argumentativos y debates en X / Twitter.
    """
    if cliente is None:
        cliente = load_client_profile("lla_chascomus")

    nombre_cliente = cliente.get("nombre", "LLA Chascomús")
    restricciones = cliente.get("restricciones", [])
    hashtags_list = cliente.get("hashtags_fijos", {}).get("milei", ["#Milei", "#LLA"])
    hashtags_json = json.dumps(list(hashtags_list), ensure_ascii=False)

    restricciones_str = "\n".join(f"- {r}" for r in restricciones)

    system_prompt = f"""Eres un estratega senior de comunicación política y redes sociales en X (Twitter) para '{nombre_cliente}'.
Tu especialidad es redactar hilos de alto impacto, analíticos, con datos duros y argumentos irrefutables que generen debate y viralidad orgánica.

REGLAS DE FORMATO Y ESTILO:
{restricciones_str}
- NUNCA uses emojis si el tono es 'confrontacional' o 'serio'.
- Cada tweet individual NO DEBE superar bajo ninguna circunstancia los 280 caracteres.
- El primer tweet (Gancho / [1/{cantidad_tweets}]) debe plantear una tesis provocadora o un dato demoledor que obligue a abrir el hilo.
- Los tweets intermedios deben desglosar hechos, cifras concretas y contraponer ideas.
- El tweet final debe cerrar con una conclusión contundente, llamado al debate o RT y los hashtags oficiales.
- Tu respuesta DEBE ser ÚNICAMENTE un objeto JSON válido con comillas dobles según el esquema solicitado.
"""

    user_prompt = f"""Genera un hilo argumental de {cantidad_tweets} tweets para X (Twitter).

PARÁMETROS:
- Tema central: {tema if tema else 'Análisis y postura política'}
- Tono requerido: {tono}
- Cantidad de tweets: {cantidad_tweets}
- Hashtags a incluir en el cierre: {', '.join(hashtags_list)}

TEXTO FUENTE TRANSCRIPTO:
\"\"\"
{texto_fuente.strip()}
\"\"\"

ESQUEMA JSON REQUERIDO (Usa estrictamente comillas dobles válidas en JSON):
{{
  "titulo_hilo": "Título o concepto central del hilo",
  "gancho": "Texto completo del primer tweet con gancho [1/{cantidad_tweets}]",
  "total_tweets": {cantidad_tweets},
  "tweets": [
    {{
      "num": 1,
      "texto": "Texto del tweet 1 que sirve de gancho [1/{cantidad_tweets}]",
      "caracteres": 150,
      "enfoque": "gancho"
    }},
    {{
      "num": 2,
      "texto": "Texto del tweet 2 con datos y desarrollo [2/{cantidad_tweets}]",
      "caracteres": 210,
      "enfoque": "dato_duro"
    }}
  ],
  "hashtags": {hashtags_json},
  "cta": "Llamado final a la acción / debate"
}}
"""

    return {
        "system": system_prompt.strip(),
        "user": user_prompt.strip(),
        "cantidad_tweets": cantidad_tweets,
        "tono": tono,
        "red": "twitter"
    }
