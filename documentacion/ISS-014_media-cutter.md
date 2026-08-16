# ISS-014 — Media Cutter (Clips .mp4, Subtítulos .srt/.vtt)

**Tipo:** `feature`
**Sesión:** 4
**Prioridad:** Alta
**Dependencias:** ISS-001, ISS-002
**Branch:** `feature/ISS-014_media-cutter`

---

## Descripción

Implementar el módulo de manipulación de medios que permite cortar clips de video
o audio a partir de un rango de timestamps, normalizar el volumen del audio, y
exportar subtítulos sincronizados en formatos .srt y .vtt compatibles con CapCut,
YouTube y plataformas de redes sociales.

## Criterios de Aceptación

- [ ] Corte de clip `.mp4` dado `[start_sec, end_sec]` sin re-encodear (copia de stream)
- [ ] Extracción de pista de audio `.mp3` de un rango de tiempo
- [ ] Normalización de volumen a -16 LUFS (estándar de redes sociales) con FFmpeg
- [ ] Eliminación de silencios superiores a 2 segundos (opcional, configurable)
- [ ] Generación de archivo `.srt` sincronizado desde lista de segmentos
- [ ] Generación de archivo `.vtt` (WebVTT) para YouTube/web
- [ ] Todos los archivos guardados en `output/{proyecto}/clips/`
- [ ] Metadatos del clip (duración, tamaño, formato) retornados en el resultado

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/core/media_cutter.py`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido re-encodear video si la operación puede hacerse con copia de stream (`-c copy`)
- Prohibido modificar el archivo de video original
- Prohibido guardar fuera de `output/{proyecto}/clips/`
- Prohibido usar `subprocess.run` sin `check=True` y captura de stderr

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.core.media_cutter import MediaCutter
cutter = MediaCutter()

# Test de generación de SRT
segments = [
    {'start': 0.0, 'end': 3.5, 'text': 'El deficit era del cinco por ciento.'},
    {'start': 3.5, 'end': 7.2, 'text': 'Hoy estamos en superavit primario.'},
]
srt = cutter.to_srt(segments)
assert '00:00:00,000 --> 00:00:03,500' in srt, 'Formato SRT incorrecto'
assert 'superavit' in srt, 'Contenido SRT incorrecto'
print('OK: SRT generado correctamente')
print(srt)
"
```

---

## Especificación de la Interfaz

```python
class MediaCutter:

    def cut_video(
        self,
        source_path: str,
        start_sec: float,
        end_sec: float,
        proyecto: str,
        nombre: str = None
    ) -> dict:
        """
        Corta un fragmento de video.
        Retorna: {"path": "output/.../clip_01.mp4", "duration": 62.5, "size_mb": 18.3}
        """

    def extract_audio(
        self,
        source_path: str,
        start_sec: float,
        end_sec: float,
        normalize: bool = True,    # normalizar a -16 LUFS
        remove_silence: bool = False
    ) -> dict:
        """Extrae y normaliza una pista de audio en .mp3."""

    def to_srt(
        self,
        segments: list[dict],
        start_offset: float = 0.0   # para ajustar timestamps al rango del clip
    ) -> str:
        """
        Genera el contenido del archivo .srt.
        Formato: "HH:MM:SS,mmm --> HH:MM:SS,mmm"
        """

    def to_vtt(
        self,
        segments: list[dict],
        start_offset: float = 0.0
    ) -> str:
        """
        Genera el contenido del archivo .vtt (WebVTT para YouTube).
        Formato: "HH:MM:SS.mmm --> HH:MM:SS.mmm"
        """

    def save_subtitles(
        self,
        segments: list[dict],
        proyecto: str,
        nombre: str = "subtitulos",
        formats: list = ["srt", "vtt"]
    ) -> dict:
        """Guarda los subtítulos en disco y retorna las rutas."""
```

## Notas Técnicas

**Corte sin re-encodear (copia de stream):**
```python
# Rápido y sin pérdida de calidad
ffmpeg -ss {start} -to {end} -i {input} -c copy {output}
```

**Normalización de volumen (-16 LUFS):**
```python
ffmpeg -i {input} -af loudnorm=I=-16:TP=-1.5:LRA=11 {output}
```

**Eliminación de silencios:**
```python
ffmpeg -i {input} -af silenceremove=stop_periods=-1:stop_duration=2:stop_threshold=-50dB {output}
```
