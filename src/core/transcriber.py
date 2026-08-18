"""Motor de transcripción dual: Groq Whisper (cloud primario) + faster-whisper (local fallback)."""
import os
import time
import subprocess
from pathlib import Path
from groq import Groq
from src.config.settings import GROQ_API_KEY, MODELS, TEMP_DIR
from src.core.audio_extractor import get_audio_info, check_ffmpeg

def _prepare_audio_chunks_for_groq(audio_path: str, max_chunk_duration_sec: int = 600) -> list[tuple[str, float, bool]]:
    """
    Prepara uno o más fragmentos de audio optimizados en MP3 mono para Groq Whisper (límite 25 MB).
    Retorna lista de tuplas: (ruta_audio, offset_inicio_segundos, es_archivo_temporal).
    """
    audio_file_path = Path(audio_path).resolve()
    if not audio_file_path.exists():
        raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

    # Si FFmpeg no está instalado, retorna el archivo original como fallback
    if not check_ffmpeg():
        return [(str(audio_file_path), 0.0, False)]

    try:
        info = get_audio_info(str(audio_file_path))
        duration = float(info.get("duration", 0.0))
    except Exception:
        duration = 0.0

    timestamp = int(time.time() * 1000)

    # Caso 1: Audio corto (< 10 minutos)
    if 0 < duration <= max_chunk_duration_sec:
        # Si ya es un mp3/m4a pequeño (< 20 MB), no re-comprimir
        if audio_file_path.suffix.lower() in [".mp3", ".m4a"] and audio_file_path.stat().st_size < 20 * 1024 * 1024:
            return [(str(audio_file_path), 0.0, False)]
        
        # Convertir a MP3 mono 48k liviano
        compressed_path = TEMP_DIR / f"groq_opt_{timestamp}.mp3"
        cmd = [
            "ffmpeg", "-y",
            "-i", str(audio_file_path),
            "-vn", "-acodec", "libmp3lame",
            "-b:a", "48k", "-ac", "1", "-ar", "16000",
            str(compressed_path)
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0 and compressed_path.exists():
            return [(str(compressed_path), 0.0, True)]

    # Caso 2: Audio largo o duración desconocida -> Dividir en fragmentos de 10 minutos
    if duration > max_chunk_duration_sec:
        chunks = []
        start_sec = 0.0
        chunk_idx = 0

        while start_sec < duration:
            dur_slice = min(float(max_chunk_duration_sec), duration - start_sec)
            chunk_file = TEMP_DIR / f"groq_chunk_{timestamp}_{chunk_idx}.mp3"

            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start_sec),
                "-t", str(dur_slice),
                "-i", str(audio_file_path),
                "-vn", "-acodec", "libmp3lame",
                "-b:a", "48k", "-ac", "1", "-ar", "16000",
                str(chunk_file)
            ]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode == 0 and chunk_file.exists():
                chunks.append((str(chunk_file), start_sec, True))
            
            start_sec += dur_slice
            chunk_idx += 1

        if chunks:
            return chunks

    # Fallback por defecto si no se pudo comprimir o cortar
    return [(str(audio_file_path), 0.0, False)]


def transcribe_with_groq(audio_path: str, language: str = "es") -> list[dict]:
    """
    Transcribe audio usando Groq Whisper Cloud API con soporte transparente para audios largos.
    Comprime y segmenta automáticamente para no exceder el límite de 25 MB por request de Groq.
    """
    key = os.getenv("GROQ_API_KEY", GROQ_API_KEY)
    if not key:
        raise ValueError("GROQ_API_KEY no configurada en las variables de entorno.")

    client = Groq(api_key=key)
    audio_file_path = Path(audio_path).resolve()
    
    if not audio_file_path.exists():
        raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

    # Preparar fragmentos optimizados
    chunks = _prepare_audio_chunks_for_groq(str(audio_file_path))
    all_segments = []
    seg_id_counter = 0

    try:
        for chunk_path, offset_sec, is_temp in chunks:
            with open(chunk_path, "rb") as f:
                response = client.audio.transcriptions.create(
                    file=f,
                    model=MODELS["groq"]["whisper"],
                    language=language,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            # Parsea la respuesta verbose_json de Groq y añade el offset temporal
            if hasattr(response, "segments") and response.segments:
                for seg in response.segments:
                    start = getattr(seg, "start", None) if not isinstance(seg, dict) else seg.get("start", 0.0)
                    end = getattr(seg, "end", None) if not isinstance(seg, dict) else seg.get("end", 0.0)
                    text = getattr(seg, "text", "") if not isinstance(seg, dict) else seg.get("text", "")
                    
                    all_segments.append({
                        "id": seg_id_counter,
                        "start": round(float(start or 0.0) + offset_sec, 2),
                        "end": round(float(end or 0.0) + offset_sec, 2),
                        "text": str(text).strip()
                    })
                    seg_id_counter += 1

            elif hasattr(response, "text") and response.text:
                all_segments.append({
                    "id": seg_id_counter,
                    "start": round(offset_sec, 2),
                    "end": round(offset_sec + 10.0, 2),
                    "text": str(response.text).strip()
                })
                seg_id_counter += 1

    finally:
        # Limpieza de archivos temporales generados para la API
        for chunk_path, _, is_temp in chunks:
            if is_temp and os.path.exists(chunk_path):
                try:
                    os.remove(chunk_path)
                except OSError:
                    pass

    return all_segments

def transcribe_with_local(audio_path: str, language: str = "es", model_size: str = "medium") -> list[dict]:
    """
    Transcribe audio usando faster-whisper en CPU local (fallback offline).
    """
    from faster_whisper import WhisperModel
    
    audio_file_path = Path(audio_path).resolve()
    if not audio_file_path.exists():
        raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

    # Configuración optimizada para CPU AMD
    model = WhisperModel(
        model_size,
        device=MODELS["whisper_local"]["device"],
        compute_type=MODELS["whisper_local"]["compute_type"]
    )

    raw_segments, info = model.transcribe(
        str(audio_file_path),
        language=language,
        beam_size=5,
        vad_filter=True
    )

    segments = []
    for idx, seg in enumerate(raw_segments):
        segments.append({
            "id": idx,
            "start": round(float(seg.start), 2),
            "end": round(float(seg.end), 2),
            "text": str(seg.text).strip()
        })

    return segments

def transcribe(
    audio_path: str,
    language: str = "es",
    model_size: str = "medium",
    engine: str = "auto"
) -> dict:
    """
    Función principal de transcripción con failover automático.
    
    Parámetros:
        audio_path: Ruta al archivo WAV/MP3.
        language: Código de idioma ('es', 'en').
        model_size: Modelo para faster-whisper local ('tiny', 'base', 'medium').
        engine: 'auto' (Groq -> local fallback), 'groq' o 'local'.
    """
    audio_file_path = Path(audio_path).resolve()
    if not audio_file_path.exists():
        raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

    start_time = time.time()
    engine_used = ""
    segments = []
    error_groq = None

    if engine in ["auto", "groq"]:
        try:
            segments = transcribe_with_groq(audio_path, language=language)
            engine_used = f"Groq ({MODELS['groq']['whisper']})"
        except Exception as e:
            error_groq = str(e)
            if engine == "groq":
                raise RuntimeError(f"Error en transcripción con Groq: {error_groq}")
            # Si es 'auto', continúa con el fallback local
            print(f"[Aviso] Groq falló o cuota agotada ({error_groq}). Activando fallback local faster-whisper...")

    if not segments and (engine == "local" or engine == "auto"):
        segments = transcribe_with_local(audio_path, language=language, model_size=model_size)
        engine_used = f"faster-whisper local ({model_size})"

    elapsed_time = round(time.time() - start_time, 2)
    full_text = " ".join(s["text"] for s in segments if s.get("text"))

    return {
        "engine_used": engine_used,
        "language": language,
        "elapsed_seconds": elapsed_time,
        "total_segments": len(segments),
        "total_words": len(full_text.split()),
        "segments": segments,
        "text": full_text
    }

def get_engine_status() -> dict:
    """Retorna el estado de disponibilidad de los motores de transcripción."""
    key = os.getenv("GROQ_API_KEY", GROQ_API_KEY)
    return {
        "groq_available": bool(key),
        "groq_model": MODELS["groq"]["whisper"],
        "local_available": True,
        "local_default_model": MODELS["whisper_local"]["default_model"]
    }
