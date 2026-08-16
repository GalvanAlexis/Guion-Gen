# ISS-008 — Script Generator (Orquestador de Guiones)

**Tipo:** `feature`
**Sesión:** 2
**Prioridad:** Alta
**Dependencias:** ISS-006, ISS-007
**Branch:** `feature/ISS-008_script-generator`

---

## Descripción

Implementar el orquestador central que coordina la generación de guiones:
recibe los segmentos de la transcripción y los parámetros de configuración
(red social, tono, tema, duración, perfil de cliente) y devuelve el guion
estructurado listo para mostrar en la UI y descargar.

## Criterios de Aceptación

- [ ] `script_generator.py` acepta `segments`, `red`, `tono`, `tema`, `cliente_profile`
- [ ] Enruta al módulo de prompt correcto según la red social elegida
- [ ] Inyecta el texto del rango de la transcripción (usa `markdown_builder.extract_range`)
- [ ] Llama a `api_manager.generate()` con el prompt armado
- [ ] Parsea la respuesta JSON del LLM de forma robusta (con fallback si el JSON es inválido)
- [ ] Guarda el guion generado en `output/{proyecto}/guion_{red}_{timestamp}.md`
- [ ] Retorna el dict estructurado para renderizado en la UI
- [ ] Soporta generación de múltiples variantes (misma configuración, distintos outputs)

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/scripts/script_generator.py`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido llamar APIs directamente (usar `api_manager`)
- Prohibido modificar los módulos de prompts individuales
- Prohibido procesar más de 4.000 palabras de texto fuente por llamada (truncar si excede)
- Prohibido dejar archivos de guion sin guardar en disco

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.scripts.script_generator import ScriptGenerator
gen = ScriptGenerator()
# Test sin API real (usa mock o verifica solo la estructura)
result = gen.generate(
    segments=[{'start': 0, 'end': 10, 'text': 'El deficit era del 5 del PBI.'}],
    red='twitter',
    tono='confrontacional',
    tema='deficit fiscal',
    proyecto='test-proyecto'
)
assert 'red' in result, 'Falta campo red'
assert 'contenido' in result, 'Falta campo contenido'
print('OK: ScriptGenerator funciona correctamente')
"
```

---

## Especificación de la Interfaz

```python
class ScriptGenerator:

    def generate(
        self,
        segments: list[dict],
        red: str,              # "tiktok" | "twitter" | "instagram" | "facebook"
        tono: str,             # "confrontacional" | "educativo" | "motivacional" | "urgente"
        tema: str,             # descripción libre del tema a desarrollar
        proyecto: str,         # nombre del proyecto activo
        duracion: int = 60,    # segundos (solo para TikTok/Reels)
        rango: tuple = None,   # (inicio_seg, fin_seg) en segundos
        cliente_id: str = "lla_chascomus"
    ) -> dict:
        """
        Retorna:
        {
            "red": "twitter",
            "tono": "confrontacional",
            "tema": "deficit fiscal",
            "contenido": {...},  # estructura específica según la red
            "archivo": "output/proyecto/guion_twitter_20260816.md",
            "tokens_usados": 1423,
            "proveedor": "gemini"
        }
        """

    def generate_variants(
        self,
        n: int = 3,
        **kwargs
    ) -> list[dict]:
        """Genera N variantes del mismo guion para elegir la mejor."""
```
