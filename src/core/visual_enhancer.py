"""Módulo para enriquecer visualmente el brief con IA."""
import json
from src.config.api_manager import api_manager

# Columnas por tipo de contenido
COLS_IMAGEN = ["Nro", "Título", "Descripción Visual", "Dato / Métrica Clave"]
COLS_VIDEO = ["Nro", "Descripción Visual", "Texto en Pantalla", "Movimiento de Cámara", "Duración (s)"]


def generate_table_items(
    narrative_prompt: str,
    tipo_contenido: str,
    cant_items: int,
    estilo: dict,
    cliente: dict
) -> list[dict]:
    """
    Llama al LLM para auto-completar las filas de la tabla (láminas o escenas).
    Retorna una lista de dicts con las claves correctas según el tipo de contenido.
    """
    nombre_cliente = cliente.get("nombre", "Genérico")
    estilo_nombre = estilo.get("nombre", "Editorial")
    
    if tipo_contenido == "Imagen":
        item_type = f"{cant_items} láminas de carrusel para imagen"
        cols_desc = "Nro (número entero), Titulo (título corto de la lámina), Descripcion_Visual (descripción detallada del contenido visual y texto a mostrar), Dato_Metrica_Clave (estadística o dato impactante si aplica, si no poner string vacío)"
        cols_keys = ["Nro", "Título", "Descripción Visual", "Dato / Métrica Clave"]
    else:
        item_type = f"{cant_items} escenas de video"
        cols_desc = "Nro (número entero), Descripcion_Visual (qué se ve en pantalla, plano, composición), Texto_en_Pantalla (texto o subtítulo que aparece), Movimiento_Camara (tipo de plano y movimiento, ej: 'Zoom in desde plano general', 'Paneo lento de izquierda a derecha'), Duracion_s (duración en segundos, número entero)"
        cols_keys = ["Nro", "Descripción Visual", "Texto en Pantalla", "Movimiento de Cámara", "Duración (s)"]

    prompt = f"""Sos un director creativo político para '{nombre_cliente}'.

Contexto narrativo del contenido:
{narrative_prompt[:2000] if narrative_prompt else "Sin contexto narrativo previo."}

Línea visual/estética: {estilo_nombre}

Generá exactamente {item_type} coherentes con ese contexto narrativo y línea visual.
Respondé ÚNICAMENTE con un JSON válido con esta estructura exacta:

{{
  "items": [
    {{{ cols_desc } }},
    ...
  ]
}}

Las claves del JSON DEBEN ser exactamente: {[k.replace(" ", "_").replace("/", "_") for k in cols_keys]}
No uses tildes en las CLAVES del JSON. Solo en los VALORES.
Generá exactamente {cant_items} objetos en el array "items"."""

    try:
        result = api_manager.generate_json(
            prompt=prompt,
            system_prompt="Sos un director creativo político experto. Respondés siempre con JSON válido.",
            temperature=0.7,
            max_tokens=3000
        )
        items_raw = result.get("data", {}).get("items", [])
        
        # Normalizar claves al formato de columnas esperadas
        key_map = {
            # Imagen
            "Nro": "Nro",
            "Titulo": "Título",
            "Titulo_": "Título",
            "Descripcion_Visual": "Descripción Visual",
            "Dato_Metrica_Clave": "Dato / Métrica Clave",
            # Video
            "Texto_en_Pantalla": "Texto en Pantalla",
            "Movimiento_Camara": "Movimiento de Cámara",
            "Duracion_s": "Duración (s)"
        }
        
        normalized = []
        for i, item in enumerate(items_raw):
            row = {}
            for raw_key, val in item.items():
                mapped = key_map.get(raw_key, raw_key)
                row[mapped] = val
            # Asegurar que el Nro sea correcto
            row["Nro"] = i + 1
            normalized.append(row)
        
        return normalized[:cant_items]
    except Exception as e:
        return []


def enhance_visual_prompt(
    brief_md: str,
    tipo_contenido: str,
    estilo: dict,
    red_social: str,
    dimensiones: str,
    cliente: dict
) -> str:
    """
    Toma el brief visual en formato Markdown y lo enriquece con lenguaje natural
    y detalles técnicos (artísticos, cinematográficos o de diseño).
    
    Retorna el prompt definitivo mejorado en formato Markdown.
    """
    nombre_cliente = cliente.get("nombre", "Genérico")
    estilo_nombre = estilo.get("nombre", "Editorial")
    estilo_uso = estilo.get("uso", "")

    if tipo_contenido == "Video":
        instruccion_tecnica = (
            "Para cada escena, expandí con detalles técnicos de cine: "
            "tipo de plano (primer plano, plano general, plano medio), "
            "movimiento de cámara (travelling, paneo, zoom, steadicam), "
            "iluminación (luz natural, contraluz, fill light, luz dura), "
            "ritmo de edición (corte seco, fundido, transición dinámica), "
            "música o diseño sonoro (SFX, música épica, silencio dramático)."
        )
    else:
        instruccion_tecnica = (
            "Para cada lámina, expandí con detalles técnicos de diseño gráfico: "
            "paleta de colores exacta (colores primarios, secundarios y de acento con hexadecimales), "
            "tipografía (familia, peso, tamaño relativo), "
            "composición (regla de tercios, espacio negativo, jerarquía visual), "
            "elementos gráficos decorativos (líneas, íconos, texturas, overlays)."
        )

    prompt = f"""Sos un director creativo político senior trabajando para '{nombre_cliente}'.
Tu tarea es MEJORAR y ENRIQUECER el siguiente brief visual en Markdown, SIN perder su estructura.

BRIEF ORIGINAL:
---
{brief_md}
---

REGLAS DE MEJORA:
1. Reescribí la sección "Guion Narrativo Base" con lenguaje más natural, emotivo y directo. Conservá todos los datos y hechos.
2. Enriquecí la sección "Estructura de Contenido": {instruccion_tecnica}
3. Expandí la "Instrucción al LLM" con instrucciones técnicas específicas para la plataforma '{red_social}' en formato {dimensiones}, usando la línea estética '{estilo_nombre}' ({estilo_uso}).
4. Agregá una nueva sección al final: "## Referentes Visuales" con 3 referencias de estilo concretas (director de cine, marca, campaña política o artista gráfico reconocido).

FORMATO DE SALIDA:
- Devolvé el documento Markdown completo y mejorado.
- No incluyas texto fuera del Markdown.
- Usá los mismos headers (##, ###, **negrita**, tablas) del original."""

    try:
        result = api_manager.generate(
            prompt=prompt,
            system_prompt="Sos un director creativo experto. Respondés con Markdown limpio.",
            temperature=0.75,
            max_tokens=4096
        )
        return result["text"].strip()
    except Exception as e:
        return f"{brief_md}\n\n> **Error al mejorar el brief:** {str(e)}"
