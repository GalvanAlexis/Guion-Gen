# ISS-002 — Motor de Transcripción Dual

**Tipo:** `feature`
**Sesión:** 1
**Prioridad:** Alta
**Dependencias:** ISS-001, ISS-003
**Branch:** `feature/ISS-002_motor-transcripcion-dual`

---

## Descripción

Implementar el motor de transcripción con arquitectura de dos niveles:
**primario** en la nube con Groq Whisper (ultra rápido, ~60s para 50 min de audio)
y **fallback** local con `faster-whisper` en CPU (sin CUDA, AMD).

El módulo debe seleccionar automáticamente el motor disponible y exponer
una interfaz unificada independientemente del backend usado.

## Criterios de Aceptación

- [x] `transcriber.py` expone la función `transcribe(audio_path, language="es")` unificada
- [x] Motor Groq Whisper funciona cuando `GROQ_API_KEY` está configurada
- [x] Fallback a `faster-whisper` automático cuando Groq falla o la key no existe
- [x] Resultado incluye: lista de segmentos con `start`, `end`, `text` en segundos
- [x] Soporte de selección de modelo local: `tiny`, `base`, `medium`
- [x] Log en consola indica qué motor fue usado
- [x] Manejo de errores con mensaje claro en caso de fallo total
- [x] Test con archivo de audio de muestra genera transcripción no vacía

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/core/transcriber.py`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido modificar `requirements.txt` (ya definido en ISS-001)
- Prohibido llamar a APIs distintas de Groq y faster-whisper
- Prohibido escribir en disco dentro de este módulo (responsabilidad de ISS-004)
- Prohibido instalar dependencias adicionales

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.core.transcriber import transcribe
result = transcribe('temp/test_audio.wav', language='es')
assert len(result) > 0, 'Transcripcion vacia'
assert 'start' in result[0], 'Falta campo start'
assert 'text' in result[0], 'Falta campo text'
print(f'OK: {len(result)} segmentos transcritos')
"
```

---

## Especificación de la Interfaz

```python
# Firma pública de transcriber.py

def transcribe(
    audio_path: str,
    language: str = "es",
    model_size: str = "medium",  # para faster-whisper local
    engine: str = "auto"         # "auto" | "groq" | "local"
) -> list[dict]:
    """
    Retorna lista de segmentos:
    [
        {"start": 0.0, "end": 3.5, "text": "Buenas noches a todos..."},
        {"start": 3.5, "end": 7.2, "text": "El déficit fiscal heredado..."},
        ...
    ]
    """

def get_engine_status() -> dict:
    """
    Retorna estado de disponibilidad de cada motor:
    {"groq": True, "local": True, "active_engine": "groq"}
    """
```

## Notas Técnicas

**Groq Whisper (primario):**
```python
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
with open(audio_path, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        language="es",
        response_format="verbose_json",
        timestamp_granularities=["segment"]
    )
```

**faster-whisper (fallback, CPU AMD):**
```python
from faster_whisper import WhisperModel
model = WhisperModel("medium", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_path, language="es", beam_size=5)
```

Groq límite gratuito: **28.800 segundos de audio por hora** (8 horas de audio/hora).
