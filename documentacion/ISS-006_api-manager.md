# ISS-006 — API Manager (Rotación Gemini/Groq)

**Tipo:** `feature`
**Sesión:** 2
**Prioridad:** Alta
**Dependencias:** ISS-001
**Branch:** `feature/ISS-006_api-manager`

---

## Descripción

Implementar el gestor centralizado de APIs que maneja la rotación automática entre
Google Gemini Flash (primario) y Groq LLaMA (fallback). El módulo detecta errores
de cuota (429), cambia de proveedor de forma transparente y expone el estado actual
de disponibilidad de cada API para mostrarlo en la barra de estado de la UI.

## Criterios de Aceptación

- [x] `api_manager.py` expone función `generate(prompt, system_prompt)` unificada
- [x] Gemini Flash se usa como proveedor cuando la key está disponible
- [x] Fallback automático a Groq cuando Gemini no está disponible o falla
- [x] Estado de disponibilidad consultable con `get_status()`
- [x] Soporte de `temperature` y `max_tokens` configurables
- [x] Log de cada llamada: proveedor usado, tokens consumidos, latencia
- [x] Si ambos fallan, levanta excepción con mensaje claro al usuario
- [x] Keys leídas desde variables de entorno (nunca hardcodeadas)

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/config/api_manager.py`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido loggear o imprimir las API keys en ningún formato
- Prohibido usar modelos distintos a los especificados
- Prohibido hacer reintentos infinitos (máximo 2 intentos por proveedor)
- Prohibido modificar archivos `.env`

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.config.api_manager import APIManager
mgr = APIManager()
status = mgr.get_status()
print('Gemini:', status['gemini'])
print('Groq:', status['groq'])
assert 'active' in status, 'Falta campo active'
print('OK: APIManager inicializado correctamente')
"
```

---

## Especificación de la Interfaz

```python
class APIManager:
    """Gestor de APIs con rotación automática y failover."""

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """
        Genera texto usando el proveedor activo.
        Hace fallback automático si el primario falla.
        Retorna el texto generado como string.
        """

    def get_status(self) -> dict:
        """
        Retorna estado en tiempo real:
        {
            "gemini": {"available": True, "model": "gemini-2.0-flash"},
            "groq": {"available": True, "model": "llama-3.3-70b-versatile"},
            "active": "gemini",
            "session_tokens": 12453
        }
        """
```

## Modelos Configurados

| Proveedor | Modelo | Rol | Costo |
|---|---|---|---|
| Google Gemini | `gemini-2.0-flash` | Primario | ~$0.0002/1K tokens |
| Groq | `llama-3.3-70b-versatile` | Fallback | Gratis (límite: 14.400 tokens/min) |
| Groq | `whisper-large-v3` | Transcripción | Gratis (28.800 seg/hora) |
