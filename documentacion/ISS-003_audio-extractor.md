# ISS-003 — Audio Extractor (FFmpeg + yt-dlp)

**Tipo:** `feature`
**Sesión:** 1
**Prioridad:** Alta
**Dependencias:** ISS-001
**Branch:** `feature/ISS-003_audio-extractor`

---

## Descripción

Implementar el módulo de extracción y normalización de audio que acepta tres
fuentes distintas de entrada: archivo local (MP4, MKV, MOV, MP3, WAV, M4A),
URL de YouTube/plataformas compatibles con yt-dlp, y texto plano (bypass — devuelve
None indicando que no hay audio que procesar).

La salida siempre es un archivo WAV mono a 16kHz en la carpeta `temp/`.
Este formato es el óptimo para Whisper y para faster-whisper.

## Criterios de Aceptación

- [ ] `audio_extractor.py` acepta ruta de archivo local y extrae audio a WAV 16kHz mono
- [ ] `audio_extractor.py` acepta URL de YouTube y descarga + extrae el audio
- [ ] Archivos de audio puros (.mp3, .wav) se normalizan directamente sin extracción
- [ ] Duración del archivo extraído se retorna junto al path
- [ ] Limpieza automática de archivos temporales al finalizar el proceso
- [ ] Manejo de error claro si FFmpeg no está instalado
- [ ] Manejo de error claro si la URL de YouTube no es válida o el video es privado
- [ ] El path de salida siempre es `temp/{nombre_proyecto}_{timestamp}.wav`

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/core/audio_extractor.py`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido escribir en directorios fuera de `temp/` y `output/`
- Prohibido hacer requests HTTP directos (usar yt-dlp para URLs)
- Prohibido dejar archivos temporales sin limpiar en casos de error
- Prohibido usar subprocess sin captura de stderr

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.core.audio_extractor import extract_audio
result = extract_audio('temp/test_video.mp4')
assert result['path'].endswith('.wav'), 'Formato incorrecto'
assert result['duration'] > 0, 'Duracion invalida'
assert result['sample_rate'] == 16000, 'Sample rate incorrecto'
print(f'OK: Audio extraido - {result[\"duration\"]:.1f}s en {result[\"path\"]}')
"
```

---

## Especificación de la Interfaz

```python
# Firma pública de audio_extractor.py

def extract_audio(
    source: str,           # ruta local o URL de YouTube
    project_name: str = "proyecto",
    cleanup: bool = True   # eliminar archivo temporal al finalizar
) -> dict:
    """
    Retorna:
    {
        "path": "temp/proyecto_20260816.wav",
        "duration": 3012.5,   # segundos
        "sample_rate": 16000,
        "channels": 1,
        "source_type": "file" | "url" | "text"
    }
    """

def check_ffmpeg() -> bool:
    """Verifica que FFmpeg esté disponible en el PATH del sistema."""

def get_video_info(source: str) -> dict:
    """Retorna metadatos básicos del video antes de procesar (duración, título, formato)."""
```

## Notas Técnicas

**Extracción con ffmpeg-python:**
```python
import ffmpeg
(
    ffmpeg
    .input(input_path)
    .output(output_path, ar=16000, ac=1, acodec='pcm_s16le')
    .overwrite_output()
    .run(capture_stdout=True, capture_stderr=True)
)
```

**Descarga con yt-dlp:**
```python
import yt_dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'temp/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
```
