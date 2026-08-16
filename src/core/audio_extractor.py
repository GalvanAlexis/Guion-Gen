"""Módulo de extracción y normalización de audio con FFmpeg y yt-dlp."""
import os
import json
import shutil
import subprocess
import time
from pathlib import Path
import yt_dlp
from src.config.settings import TEMP_DIR

def check_ffmpeg() -> bool:
    """Verifica si FFmpeg está disponible en el PATH del sistema."""
    if shutil.which("ffmpeg") is not None:
        return True
    try:
        res = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return res.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_audio_info(file_path: str) -> dict:
    """Obtiene la duración y formato de un archivo multimedia usando ffprobe en formato JSON."""
    file_path = str(Path(file_path).resolve())
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        data = json.loads(result.stdout)
        
        duration = 0.0
        sample_rate = 16000
        channels = 1
        
        # Formato global
        fmt = data.get("format", {})
        if "duration" in fmt:
            try:
                duration = float(fmt["duration"])
            except (ValueError, TypeError):
                pass
                
        # Streams de audio
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "audio":
                if "sample_rate" in stream:
                    try:
                        sample_rate = int(stream["sample_rate"])
                    except (ValueError, TypeError):
                        pass
                if "channels" in stream:
                    try:
                        channels = int(stream["channels"])
                    except (ValueError, TypeError):
                        pass
                if duration == 0.0 and "duration" in stream:
                    try:
                        duration = float(stream["duration"])
                    except (ValueError, TypeError):
                        pass
                break

        return {
            "path": file_path,
            "duration": round(duration, 2),
            "sample_rate": sample_rate,
            "channels": channels,
            "size_bytes": os.path.getsize(file_path)
        }
    except Exception:
        # Fallback básico si ffprobe falla
        return {
            "path": file_path,
            "duration": 0.0,
            "sample_rate": 16000,
            "channels": 1,
            "size_bytes": os.path.getsize(file_path)
        }

def extract_audio_from_file(input_path: str, output_path: str = None, sample_rate: int = 16000) -> dict:
    """
    Extrae el audio de un archivo de video o audio local y lo normaliza a WAV 16kHz mono.
    """
    if not check_ffmpeg():
        raise RuntimeError("FFmpeg no está instalado o no se encuentra en el PATH del sistema.")

    input_file = Path(input_path).resolve()
    if not input_file.exists():
        raise FileNotFoundError(f"El archivo fuente no existe: {input_path}")

    if output_path is None:
        timestamp = int(time.time())
        output_path = TEMP_DIR / f"audio_{input_file.stem}_{timestamp}.wav"
    else:
        output_path = Path(output_path).resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Conversión directa con FFmpeg: mono (ac=1), 16kHz (ar=16000), PCM 16-bit
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_file),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ac", "1",
        "-ar", str(sample_rate),
        str(output_path)
    ]

    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        raise RuntimeError(f"Error al extraer audio con FFmpeg:\n{process.stderr}")

    info = get_audio_info(str(output_path))
    info["source_type"] = "file"
    info["original_file"] = str(input_file)
    return info

def download_youtube_audio(url: str, output_path: str = None, sample_rate: int = 16000) -> dict:
    """
    Descarga el audio de un video de YouTube y lo convierte a WAV 16kHz mono.
    """
    if not check_ffmpeg():
        raise RuntimeError("FFmpeg no está instalado o no se encuentra en el PATH del sistema.")

    timestamp = int(time.time())
    temp_download_template = str(TEMP_DIR / f"yt_dl_{timestamp}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": temp_download_template,
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info_dict)
        title = info_dict.get("title", "Video YouTube")
        duration = info_dict.get("duration", 0.0)

    # Convertir el archivo descargado a WAV 16kHz mono
    if output_path is None:
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
        safe_title = safe_title.replace(" ", "_")[:40]
        output_path = TEMP_DIR / f"yt_{safe_title}_{timestamp}.wav"
    else:
        output_path = Path(output_path).resolve()

    res = extract_audio_from_file(downloaded_file, str(output_path), sample_rate=sample_rate)

    # Limpiar descarga temporal intermedia
    if os.path.exists(downloaded_file) and downloaded_file != str(output_path):
        try:
            os.remove(downloaded_file)
        except OSError:
            pass

    res["title"] = title
    res["source_type"] = "url"
    res["url"] = url
    if res["duration"] == 0.0 and duration:
        res["duration"] = float(duration)

    return res

def extract_audio(source: str, project_name: str = "proyecto", sample_rate: int = 16000) -> dict:
    """
    Función principal unificada que extrae y normaliza audio desde archivo local o URL.
    """
    source_str = str(source).strip()
    if source_str.startswith("http://") or source_str.startswith("https://") or "youtube.com" in source_str or "youtu.be" in source_str:
        return download_youtube_audio(source_str, sample_rate=sample_rate)
    else:
        timestamp = int(time.time())
        output_path = TEMP_DIR / f"{project_name}_{timestamp}.wav"
        return extract_audio_from_file(source_str, str(output_path), sample_rate=sample_rate)
