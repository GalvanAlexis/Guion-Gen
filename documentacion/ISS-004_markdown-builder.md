# ISS-004 — Markdown Builder

**Tipo:** `feature`
**Sesión:** 1
**Prioridad:** Alta
**Dependencias:** ISS-002
**Branch:** `feature/ISS-004_markdown-builder`

---

## Descripción

Implementar el módulo que toma la lista de segmentos de la transcripción y construye
un documento Markdown (.md) estructurado y profesional. El documento debe ser útil
tanto como fuente de lectura humana como de ingesta para el motor de generación
de guiones (ISS-008).

## Criterios de Aceptación

- [x] Genera archivo `.md` con frontmatter YAML con metadatos del proyecto
- [x] Incluye tabla de contenidos con los primeros 10 segmentos como índice
- [x] Transcripción completa con timestamps `[MM:SS]` al inicio de cada bloque
- [x] Separación visual cada 5 minutos con `---` y cabecera del minuto
- [x] Función para extraer solo el texto plano de un rango `[inicio_seg, fin_seg]`
- [x] Función para extraer los N segmentos con texto más largo ("golden nuggets")
- [x] Archivo guardado en `output/{proyecto}/transcripcion.md`
- [x] Archivo también retornado como string para previsualización en la UI

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/core/markdown_builder.py`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido modificar segmentos de la transcripción (solo formatear)
- Prohibido escribir fuera de `output/{proyecto}/`
- Prohibido llamar APIs externas

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.core.markdown_builder import build_markdown, extract_range
segments = [
    {'start': 0.0, 'end': 5.0, 'text': 'Buenas noches a todos los presentes.'},
    {'start': 5.0, 'end': 12.0, 'text': 'El deficit fiscal heredado era del 5% del PBI.'},
]
md = build_markdown(segments, project='test', title='Conferencia Test')
assert '---' in md, 'Falta frontmatter YAML'
assert '[00:00]' in md, 'Falta timestamp'
assert 'El deficit' in md, 'Falta contenido'
print('OK:', len(md), 'caracteres generados')
"
```

---

## Estructura del Documento .md Generado

```markdown
---
title: "Conferencia Milei — Agosto 2026"
proyecto: "milei-conf-ago2026"
duracion: "50:23"
modelo_transcripcion: "groq/whisper-large-v3"
fecha: "2026-08-16"
segmentos: 412
palabras: 9234
---

# Conferencia Milei — Agosto 2026

## Índice Rápido (primeros 10 segmentos)

- [00:00] Buenas noches a todos los presentes...
- [00:45] El déficit fiscal heredado era del 5% del PBI...
- [01:23] La reforma del Estado no es una opción...
...

---

## Transcripción Completa

### Minuto 0

[00:00] Buenas noches a todos los presentes. Es un honor compartir...

[00:45] El déficit fiscal que heredamos era del 5% del PBI. Para ponerlo...

[01:23] La reforma del Estado no es una opción, es una obligación...

---

### Minuto 5

[05:00] Cuando hablamos de libertad económica, hablamos de devolverle...

...
```

## Especificación de la Interfaz

```python
def build_markdown(
    segments: list[dict],
    project: str,
    title: str,
    source_info: dict = None   # metadatos del audio/video original
) -> str:
    """Retorna el string completo del .md y lo guarda en output/{project}/."""

def extract_range(
    segments: list[dict],
    start_sec: float,
    end_sec: float
) -> str:
    """Retorna solo el texto del rango de tiempo indicado (para el script generator)."""

def extract_golden_nuggets(
    segments: list[dict],
    n: int = 10
) -> list[dict]:
    """Retorna los N segmentos con mayor densidad de texto (más palabras por segundo)."""
```
