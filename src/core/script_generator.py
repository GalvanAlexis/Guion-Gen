"""Orquestador principal de generación de guiones multiplataforma."""
import os
import re
import json
import unicodedata
from datetime import datetime
from pathlib import Path

from src.config.api_manager import api_manager
from src.config.settings import PUBLICATIONS_DIR, OUTPUT_DIR, load_client_profile
from src.scripts.tiktok_reels import get_tiktok_prompt
from src.scripts.twitter_threads import get_twitter_prompt
from src.scripts.social_posts import get_social_post_prompt

def slugify(text: str) -> str:
    """Convierte un texto a un slug seguro para nombres de archivo."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    return re.sub(r'[-\s]+', '-', text)[:40]

def format_script_to_markdown(data: dict, red: str) -> str:
    """Convierte el JSON estructurado de un guion en formato Markdown legible."""
    red_norm = red.lower().strip()

    if red_norm in ["tiktok", "reels", "shorts"]:
        md = [
            f"# 🎬 Guion Técnico: {data.get('titulo', 'Sin Título')}\n",
            f"- **Plataforma:** {red.upper()} (Formato 9:16 Vertical)",
            f"- **Duración estimada:** {data.get('duracion', 60)} segundos",
            f"- **Gancho inicial:** *\"{data.get('hook_texto', '')}\"*\n",
            "## 📋 Desglose Técnico en 2 Columnas\n",
            "| Tiempo | Locución (VOZ) | Indicación Visual / B-Roll | Efectos / Sonido |",
            "|---|---|---|---|"
        ]
        for s in data.get("slides", []):
            seg = s.get("seg", "")
            voz = s.get("voz", "").replace("|", "-")
            vis = s.get("visual", "").replace("|", "-")
            efe = s.get("efecto", "").replace("|", "-")
            md.append(f"| `{seg}` | {voz} | {vis} | {efe} |")

        hashtags_str = " ".join(data.get("hashtags", []))
        md.append(f"\n**Llamado a la acción (CTA):** {data.get('cta', '')}")
        md.append(f"**Hashtags recomendados:** `{hashtags_str}`")
        return "\n".join(md)

    elif red_norm in ["x", "twitter"]:
        tweets = data.get("tweets", [])
        total = data.get("total_tweets", len(tweets))
        md = [
            f"# 🧵 Hilo para X (Twitter): {data.get('titulo_hilo', 'Sin Título')}\n",
            f"- **Total de tweets:** {total}",
            f"- **Gancho de apertura:** *\"{data.get('gancho', '')}\"*\n",
            "## 📝 Secuencia de Tweets\n"
        ]
        for idx, tw in enumerate(tweets, 1):
            num = tw.get("num", idx)
            texto = tw.get("texto", "")
            chars = tw.get("caracteres", len(texto))
            enfoque = tw.get("enfoque", "")
            md.append(f"### Tweet {num}/{total} `({chars} caracteres | {enfoque})`")
            md.append(f"```text\n{texto}\n```\n")

        hashtags_str = " ".join(data.get("hashtags", []))
        md.append(f"**Cierre / CTA:** {data.get('cta', '')}")
        md.append(f"**Hashtags:** `{hashtags_str}`")
        return "\n".join(md)

    else:  # Instagram / Facebook / Carruseles
        slides = data.get("slides", [])
        total = data.get("total_slides", len(slides))
        md = [
            f"# 🖼 Carrusel para {red.upper()}: {data.get('titulo', 'Sin Título')}\n",
            f"- **Estructura:** P.A.S.C. ({total} Diapositivas 4:5)",
            f"- **Objetivo:** Retención visual y debate en comentarios\n",
            "## 📑 Diapositivas del Carrusel\n"
        ]
        for s in slides:
            num = s.get("slide_num", 1)
            tipo = s.get("tipo", "slide").upper()
            tit = s.get("titulo", "")
            cuerpo = s.get("cuerpo", "")
            dato = s.get("dato_destacado", "")
            md.append(f"### Slide {num} — [{tipo}]")
            md.append(f"**Título:** {tit}")
            if dato:
                md.append(f"**Dato Destacado:** `{dato}`")
            md.append(f"**Texto de apoyo:** {cuerpo}\n")

        md.append("---")
        md.append("## ✍️ Copy Caption para la Publicación")
        md.append(f"```text\n{data.get('copy_caption', '')}\n```\n")
        hashtags_str = " ".join(data.get("hashtags", []))
        md.append(f"**Hashtags:** `{hashtags_str}`")
        return "\n".join(md)

def generate_script(
    texto_fuente: str,
    red: str = "tiktok",
    tema: str = "",
    tono: str = "confrontacional",
    tono_refuerzo: str = "",
    duracion: int = 60,
    cantidad_slides: int = 5,
    cliente: dict = None,
    project_name: str = "proyecto_general",
    topic_timestamp: str = None
) -> dict:
    """
    Genera un guion especializado, lo parsea, lo formatea a Markdown y lo guarda en disco.
    """
    if cliente is None:
        cliente = load_client_profile("lla_chascomus")

    if tono_refuerzo:
        tono = f"{tono} - Reforzar con: {tono_refuerzo}"

    red_norm = red.lower().strip()
    if red_norm in ["tiktok", "reels", "shorts"]:
        prompt_pkg = get_tiktok_prompt(
            texto_fuente=texto_fuente,
            tono=tono,
            tema=tema,
            duracion=duracion,
            cliente=cliente
        )
        folder_red = "tiktok"
    elif red_norm in ["x", "twitter"]:
        prompt_pkg = get_twitter_prompt(
            texto_fuente=texto_fuente,
            tono=tono,
            tema=tema,
            cliente=cliente
        )
        folder_red = "x"
    elif red_norm in ["instagram", "ig"]:
        prompt_pkg = get_social_post_prompt(
            texto_fuente=texto_fuente,
            red="instagram",
            tono=tono,
            tema=tema,
            cantidad_slides=cantidad_slides,
            cliente=cliente
        )
        folder_red = "ig"
    elif red_norm in ["facebook", "fb"]:
        prompt_pkg = get_social_post_prompt(
            texto_fuente=texto_fuente,
            red="facebook",
            tono=tono,
            tema=tema,
            cantidad_slides=cantidad_slides,
            cliente=cliente
        )
        folder_red = "fb"
    else:
        raise ValueError(f"Red social '{red}' no soportada. Use 'tiktok', 'x', 'instagram' o 'facebook'.")

    user_prompt = prompt_pkg["user"]
    if topic_timestamp:
        user_prompt += f"\n\n[INSTRUCCIÓN CRÍTICA] El tema seleccionado por el usuario aparece en el timestamp exacto [{topic_timestamp}]. Por favor, focalizá el análisis y las citas textuales basándote en lo que se dice a partir de ese minuto del discurso original."

    # Llamada a LLM a través de APIManager
    res_llm = api_manager.generate_json(
        prompt=user_prompt,
        system_prompt=prompt_pkg["system"],
        temperature=0.4
    )

    data = res_llm.get("data", {})
    md_content = format_script_to_markdown(data, red=folder_red)

    # Nomenclatura contractual: AAAA-MM-DD_red_titulo-tema_numero
    today_str = datetime.now().strftime("%Y-%m-%d")
    title_raw = data.get("titulo") or data.get("titulo_hilo") or tema or "guion"
    slug_tema = slugify(title_raw)

    # Guardar en publicaciones/{red}/
    pub_dir = PUBLICATIONS_DIR / folder_red
    pub_dir.mkdir(parents=True, exist_ok=True)

    existing_files = list(pub_dir.glob(f"{today_str}_{folder_red}_{slug_tema}_*.json"))
    item_num = f"{len(existing_files) + 1:02d}"
    
    file_base = f"{today_str}_{folder_red}_{slug_tema}_{item_num}"
    json_path = pub_dir / f"{file_base}.json"
    md_path = pub_dir / f"{file_base}.md"

    # Guardar JSON y MD en publicaciones
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # Guardar copia en output/{project_name}/guiones/
    out_guiones_dir = OUTPUT_DIR / project_name / "guiones"
    out_guiones_dir.mkdir(parents=True, exist_ok=True)
    with open(out_guiones_dir / f"{folder_red}_{file_base}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "red": folder_red,
        "titulo": title_raw,
        "data": data,
        "markdown": md_content,
        "json_path": str(json_path),
        "md_path": str(md_path),
        "tokens_used": res_llm.get("tokens_used", 0),
        "latency_seconds": res_llm.get("latency_seconds", 0.0),
        "provider": res_llm.get("provider", "groq")
    }

def generate_multi_platform_scripts(
    texto_fuente: str,
    redes: list[str],
    tema: str = "",
    tono: str = "confrontacional",
    duracion: int = 60,
    cliente: dict = None,
    project_name: str = "proyecto_general",
    topic_timestamp: str = None
) -> dict:
    """
    Genera guiones para múltiples plataformas en una sola llamada.
    """
    results = {}
    for red in redes:
        results[red] = generate_script(
            texto_fuente=texto_fuente,
            red=red,
            tema=tema,
            tono=tono,
            duracion=duracion,
            cliente=cliente,
            project_name=project_name,
            topic_timestamp=topic_timestamp
        )
    return results

def generate_topic_index(texto_fuente: str) -> list[dict]:
    """
    Lee la transcripción completa y extrae un índice de los temas clave tratados.
    Retorna una lista de diccionarios con 'tema' y 'timestamps'.
    """
    sys_prompt = (
        "Eres un analizador de conferencias y videos. "
        "Tu objetivo es leer una transcripción con timestamps y extraer los 5 a 10 temas principales tratados.\n"
        "Si un tema se retoma en varios momentos distintos del video, agrúpalos en una lista de rangos.\n"
        "Debes responder ESTRICTAMENTE con un objeto JSON válido con la siguiente estructura:\n"
        "{\"data\": [{\"tema\": \"Título corto del tema\", \"timestamps\": [\"MM:SS-MM:SS\", \"MM:SS-MM:SS\"]}, ...]}"
    )
    
    prompt = f"Analiza esta transcripción y extrae el índice de temas:\n\n{texto_fuente}"
    
    # Llamamos a api_manager forzando Gemini para textos gigantes y evitando el rate limit de Groq
    res = api_manager.generate_json(
        prompt=prompt,
        system_prompt=sys_prompt,
        temperature=0.2,
        max_tokens=1000,
        preferred_provider="gemini"
    )
    
    parsed = res.get("data", {})
    # Si el LLM devolvió un dict {"data": [...]}, extraemos la lista
    if isinstance(parsed, dict) and "data" in parsed:
        return parsed["data"]
    # Si devolvió directamente la lista [...]
    elif isinstance(parsed, list):
        return parsed
    
    return []

def update_script_from_markdown(guion_actual: dict, edited_md: str) -> dict:
    """
    Intenta extraer las secciones editadas del markdown (para láminas de carrusel y TikTok)
    y sincronizarlas con el diccionario 'data' para que la vista previa visual se actualice.
    """
    import re
    red = guion_actual.get("red", "tiktok").lower()
    data = guion_actual.get("data", {})
    
    # 1. Actualizar TikTok / Reels
    if red in ["tiktok", "reels", "shorts"]:
        slides = []
        for line in edited_md.split('\n'):
            line = line.strip()
            if line.startswith('|') and not line.startswith('|---') and not line.startswith('| Tiempo'):
                parts = [p.strip() for p in line.split('|')]
                # parts = ['', 'tiempo', 'voz', 'visual', 'efecto', '']
                if len(parts) >= 5:
                    slides.append({
                        "seg": parts[1].replace('`', '').strip(),
                        "voz": parts[2],
                        "visual": parts[3],
                        "efecto": parts[4]
                    })
        if slides:
            data["slides"] = slides
            
    # 2. Actualizar Instagram / Facebook (Carrusel)
    elif red in ["ig", "instagram", "fb", "facebook"]:
        slides = []
        slide_blocks = re.split(r'### Slide \d+', edited_md)[1:]
        for idx, block in enumerate(slide_blocks, 1):
            tipo_match = re.search(r'—\s*\[(.*?)\]', block)
            tipo = tipo_match.group(1).strip() if tipo_match else "slide"
            
            tit_match = re.search(r'\*\*Título:\*\*\s*(.+)', block)
            titulo = tit_match.group(1).strip() if tit_match else ""
            
            dato_match = re.search(r'\*\*Dato Destacado:\*\*\s*`?(.*?)`?', block)
            dato = dato_match.group(1).replace('`', '').strip() if dato_match else ""
            
            cuerpo_match = re.search(r'\*\*Texto de apoyo:\*\*\s*(.+)', block)
            cuerpo = cuerpo_match.group(1).strip() if cuerpo_match else ""
            
            slides.append({
                "slide_num": idx,
                "tipo": tipo,
                "titulo": titulo,
                "dato_destacado": dato,
                "cuerpo": cuerpo
            })
        if slides:
            data["slides"] = slides
            
        copy_match = re.search(r'## ✍️ Copy Caption para la Publicación\s*```text\s*(.*?)\s*```', edited_md, re.DOTALL)
        if copy_match:
            data["copy_caption"] = copy_match.group(1).strip()

    # 3. Actualizar Twitter (Hilos)
    elif red in ["x", "twitter"]:
        tweets = []
        tweet_blocks = re.split(r'### Tweet \d+', edited_md)[1:]
        for idx, block in enumerate(tweet_blocks, 1):
            text_match = re.search(r'```text\s*(.*?)\s*```', block, re.DOTALL)
            texto = text_match.group(1).strip() if text_match else ""
            if texto:
                tweets.append({
                    "num": idx,
                    "texto": texto,
                    "caracteres": len(texto),
                    "enfoque": "Editado"
                })
        if tweets:
            data["tweets"] = tweets

    guion_actual["data"] = data
    guion_actual["markdown"] = edited_md
    return guion_actual
