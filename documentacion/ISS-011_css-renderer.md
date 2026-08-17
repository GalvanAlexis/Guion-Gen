# ISS-011 — CSS Renderer (HTML → Playwright → PNG)

**Tipo:** `feature`
**Sesión:** 3
**Prioridad:** Alta
**Dependencias:** ISS-010
**Branch:** `feature/ISS-011_css-renderer`

---

## Descripción

Implementar el motor de renderizado que toma un template HTML/CSS (compilado con
Jinja2) y lo convierte a imagen PNG de alta calidad mediante Playwright headless.
Es el núcleo de la generación de carruseles en "Modo CSS Rápido".

## Criterios de Aceptación

- [x] `css_renderer.py` recibe un dict con datos del slide y nombre de plantilla
- [x] Renderiza correctamente a 1080x1350px (modo 4:5) y 1080x1920px (modo 9:16)
- [x] Inspección DOM previa al screenshot (auto-escala si hay overflow de texto)
- [x] Genera PNG de alta calidad (`scale=2` → 2160x2700px efectivos)
- [x] Soporta procesamiento en lote: lista de slides → lista de PNGs
- [x] Guarda los PNG en `output/{proyecto}/carrusel/slide_{N:02d}.png`
- [x] Genera ZIP con todos los slides del carrusel listo para descarga
- [x] Tiempo de proceso visible en el log (seg/slide)
- [x] Playwright usa Chromium headless sin abrir ventana visible

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/visual/css_renderer.py`
- [NEW] `src/visual/html_renderer.py` (compilador Jinja2)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido usar `page.wait_for_timeout()` (usar espera basada en eventos DOM)
- Prohibido guardar archivos PNG fuera de `output/{proyecto}/`
- Prohibido instalar browsers adicionales (solo Chromium de Playwright)
- Prohibido dejar instancias de Playwright sin cerrar en caso de error

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.visual.css_renderer import render_slide
result = render_slide(
    template='lla_dark',
    data={'titulo': 'Test', 'cuerpo': 'Cuerpo de prueba', 'slide_num': 1, 'total_slides': 1},
    output_path='output/test/slide_01.png',
    formato='4:5'
)
import os
assert os.path.exists('output/test/slide_01.png'), 'PNG no generado'
size = os.path.getsize('output/test/slide_01.png')
assert size > 50000, f'PNG demasiado pequeño: {size} bytes'
print(f'OK: PNG generado correctamente ({size:,} bytes)')
"
```

---

## Especificación de la Interfaz

```python
def render_slide(
    template: str,          # "lla_dark" | "alerta_roja" | "estadistica"
    data: dict,             # variables Jinja2 del slide
    output_path: str,       # ruta donde guardar el PNG
    formato: str = "4:5"    # "4:5" (1080x1350) | "9:16" (1080x1920)
) -> dict:
    """
    Retorna:
    {"path": "output/.../slide_01.png", "size_bytes": 245231, "elapsed_sec": 3.2}
    """

def render_carousel(
    template: str,
    slides_data: list[dict],
    proyecto: str,
    formato: str = "4:5"
) -> dict:
    """
    Renderiza todos los slides y genera ZIP.
    Retorna:
    {
        "slides": ["output/.../slide_01.png", ...],
        "zip": "output/.../carrusel.zip",
        "total_elapsed_sec": 18.4
    }
    """
```

## Notas Técnicas

**Auto-escala de texto (anti-overflow):**
```python
# Verificar overflow y reducir fuente si es necesario
overflow = await page.evaluate("""
    () => {
        const el = document.querySelector('.slide-content');
        return el.scrollHeight > el.clientHeight;
    }
""")
if overflow:
    await page.evaluate("document.querySelector('.slide-content').style.fontSize = '85%'")
```

**Viewport por formato:**
```python
FORMATS = {
    "4:5":  {"width": 1080, "height": 1350},
    "9:16": {"width": 1080, "height": 1920},
    "1:1":  {"width": 1080, "height": 1080},
}
```
