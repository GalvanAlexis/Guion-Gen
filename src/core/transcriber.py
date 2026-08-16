"""Motor de transcripción dual: Groq Whisper (cloud primario) + faster-whisper (local fallback)."""
import os
import time
from pathlib import Path
from groq import Groq
from src.config.settings import GROQ_API_KEY, MODELS

def transcribe_with_groq(audio_path: str, language: str = "es") -> list[dict]:
    """
    Transcribe audio usando Groq Whisper Cloud API (ultra rápido, ~60s para 50 min).
    """
    key = os.getenv("GROQ_API_KEY", GROQ_API_KEY)
    if not key:
        raise ValueError("GROQ_API_KEY no configurada en las variables de entorno.")

    client = Groq(api_key=key)
    audio_file_path = Path(audio_path).resolve()
    
    if not audio_file_path.exists():
        raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

    with open(audio_file_path, "rb") as f:
        response = client.audio.transcriptions.create(
            file=f,
            model=MODELS["groq"]["whisper"],
            language=language,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    segments = []
    # Parsea la respuesta verbose_json de Groq
    if hasattr(response, "segments") and response.segments:
        for idx, seg in enumerate(response.segments):
            # seg puede ser dict o pydantic model
            start = getattr(seg, "start", None) if not isinstance(seg, dict) else seg.get("start", 0.0)
            end = getattr(seg, "end", None) if not isinstance(seg, dict) else seg.get("end", 0.0)
            text = getattr(seg, "text", "") if not isinstance(seg, dict) else seg.get("text", "")
            
            segments.append({
                "id": idx,
                "start": round(float(start or 0.0), 2),
                "end": round(float(end or 0.0), 2),
                "text": str(text).strip()
            })
    elif hasattr(response, "text") and response.text:
        # Si no hay segmentos detallados, crea un segmento global
        segments.append({
            "id": 0,
            "start": 0.0,
            "end": 0.0,
            "text": str(response.text).strip()
        })

    return segments

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
