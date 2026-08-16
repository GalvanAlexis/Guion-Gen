# ISS-012 — AI Renderer (Fondos generados por Gemini Imagen)

**Tipo:** `feature`
**Sesión:** 3
**Prioridad:** Media
**Dependencias:** ISS-006, ISS-011
**Branch:** `feature/ISS-012_ai-renderer`

---

## Descripción

Implementar el módulo de generación de fondos artísticos para carruseles mediante
Gemini Imagen. Los fondos generados por IA se montan debajo del texto y elementos
de la plantilla CSS, usando un overlay oscuro para garantizar contraste y legibilidad.
Este es el "Modo IA Creativa" del motor visual.

## Criterios de Aceptación

- [ ] `ai_renderer.py` genera un fondo PNG a partir de un prompt construido con el tema
- [ ] El prompt de imagen se construye automáticamente desde el tema y tono del guion
- [ ] Overlay oscuro aplicado sobre el fondo: `rgba(5, 5, 15, 0.82)` mínimo
- [ ] Fondo integrado en la plantilla CSS vía variable `bg_image_b64`
- [ ] Guarda el fondo generado en `temp/{proyecto}/bg_{tema_slug}.png`
- [ ] Caché local: si se generó un fondo para el mismo tema, reutiliza sin llamar la API
- [ ] Fallback automático a plantilla CSS pura si Gemini Imagen falla o no está disponible
- [ ] Costo estimado visible en el log (~$0.002 por imagen)

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/visual/ai_renderer.py`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido usar imágenes de personas reales o políticos identificables en el prompt
- Prohibido guardar fondos generados en `output/` (solo en `temp/` como caché)
- Prohibido reintentar más de 2 veces si Gemini Imagen falla
- Prohibido usar el fondo sin el overlay de oscurecimiento

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.visual.ai_renderer import AIRenderer
renderer = AIRenderer()
# Test del constructor de prompts sin llamar la API
prompt = renderer.build_image_prompt(tema='deficit fiscal', tono='confrontacional')
assert len(prompt) > 50, 'Prompt de imagen demasiado corto'
assert 'argentina' in prompt.lower() or 'political' in prompt.lower(), 'Prompt sin contexto politico'
print('OK: AIRenderer construye prompts correctamente')
"
```

---

## Especificación de la Interfaz

```python
class AIRenderer:

    def generate_background(
        self,
        tema: str,
        tono: str,
        formato: str = "4:5",    # "4:5" | "9:16"
        use_cache: bool = True
    ) -> str:
        """
        Retorna ruta al PNG del fondo generado (en temp/).
        Si el fondo ya está en caché, lo devuelve sin llamar la API.
        """

    def build_image_prompt(
        self,
        tema: str,
        tono: str
    ) -> str:
        """
        Construye el prompt descriptivo para Gemini Imagen basado en el tema.
        Ejemplo: "Abstract dark political art, Argentine economic crisis,
        deep dark background, dramatic lighting, no text, no people,
        cinematic atmosphere, 4:5 vertical format"
        """
```

## Notas Técnicas

**Prompts de imagen por tono:**

```python
TONE_PROMPTS = {
    "confrontacional": "dramatic, dark, high contrast, stormy atmosphere, tension",
    "educativo":       "clean, modern infographic background, subtle geometric shapes",
    "motivacional":    "inspirational, rays of light, dawn colors, uplifting",
    "urgente":         "red and black, alarm, critical, emergency mood, dark"
}
```

**Integración en la plantilla CSS:**
```css
.slide {
    background-image:
        linear-gradient(rgba(5,5,15,0.85), rgba(5,5,15,0.85)),
        url('data:image/png;base64,{{ bg_image_b64 }}');
    background-size: cover;
    background-position: center;
}
```
