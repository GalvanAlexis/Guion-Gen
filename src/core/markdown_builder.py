"""Módulo de construcción y exportación de documentos Markdown estructurados."""
import os
from datetime import datetime
from pathlib import Path
from src.config.settings import OUTPUT_DIR

def format_timestamp(seconds: float) -> str:
    """Convierte segundos a formato [MM:SS] o [HH:MM:SS]."""
    total_seconds = int(round(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    
    if hours > 0:
        return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"
    return f"[{minutes:02d}:{secs:02d}]"

def extract_range(segments: list[dict], start_sec: float, end_sec: float) -> str:
    """
    Extrae únicamente el texto continuo dentro del rango de tiempo especificado.
    """
    selected_texts = []
    for seg in segments:
        seg_start = seg.get("start", 0.0)
        seg_end = seg.get("end", 0.0)
        
        # Si el segmento se solapa con el rango solicitado
        if seg_end >= start_sec and seg_start <= end_sec:
            text = seg.get("text", "").strip()
            if text:
                selected_texts.append(text)
                
    return " ".join(selected_texts)

def extract_golden_nuggets(segments: list[dict], n: int = 10) -> list[dict]:
    """
    Retorna los N segmentos más relevantes o con mayor densidad de texto.
    """
    # Filtra segmentos con contenido y los ordena por longitud de palabras y duración
    valid_segments = [s for s in segments if len(s.get("text", "").split()) >= 5]
    
    # Ordenar por cantidad de palabras descendentemente
    sorted_segments = sorted(
        valid_segments,
        key=lambda s: len(s.get("text", "").split()),
        reverse=True
    )
    
    return sorted_segments[:n]

def build_markdown(
    segments: list[dict],
    project: str,
    title: str = None,
    source_info: dict = None,
    engine_used: str = "Groq Whisper"
) -> str:
    """
    Construye el documento Markdown estructurado con frontmatter YAML,
    índice rápido y bloques de tiempo de 5 minutos.
    Guarda automáticamente en output/{project}/transcripcion.md.
    """
    if not title:
        title = project.replace("_", " ").replace("-", " ").title()

    full_text = " ".join(s.get("text", "").strip() for s in segments if s.get("text"))
    words_count = len(full_text.split())
    total_segments = len(segments)
    
    last_seg_end = segments[-1].get("end", 0.0) if segments else 0.0
    duration_str = format_timestamp(last_seg_end).replace("[", "").replace("]", "")
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Frontmatter YAML
    lines = [
        "---",
        f'title: "{title}"',
        f'proyecto: "{project}"',
        f'duracion: "{duration_str}"',
        f'modelo_transcripcion: "{engine_used}"',
        f'fecha: "{date_str}"',
        f"segmentos: {total_segments}",
        f"palabras: {words_count}",
        "---",
        "",
        f"# {title}",
        "",
        "## Índice Rápido",
        ""
    ]

    # Índice con los primeros 10 segmentos
    index_limit = min(10, len(segments))
    for i in range(index_limit):
        seg = segments[i]
        ts = format_timestamp(seg.get("start", 0.0))
        txt = seg.get("text", "").strip()
        preview = txt[:80] + "..." if len(txt) > 80 else txt
        lines.append(f"- {ts} {preview}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Transcripción Completa")
    lines.append("")

    current_minute_block = -1

    for seg in segments:
        start = seg.get("start", 0.0)
        text = seg.get("text", "").strip()
        if not text:
            continue

        minute_block = int(start // 300) * 5  # Bloques de 5 minutos (0, 5, 10, 15...)
        if minute_block != current_minute_block:
            current_minute_block = minute_block
            lines.append(f"### Minuto {current_minute_block}")
            lines.append("")

        ts = format_timestamp(start)
        lines.append(f"{ts} {text}")
        lines.append("")

    content = "\n".join(lines)

    # Guardar en output/{project}/transcripcion.md
    project_dir = OUTPUT_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)
    out_file = project_dir / "transcripcion.md"
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    return content
