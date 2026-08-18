"""Módulo de manipulación de medios y exportación de subtítulos para CapCut y redes sociales."""
import os
import re
import math
import shutil
import subprocess
from pathlib import Path
from src.config.settings import OUTPUT_DIR, TEMP_DIR
from src.core.audio_extractor import check_ffmpeg, get_audio_info


def format_timestamp_srt(seconds: float) -> str:
    """Convierte segundos flotantes a formato SRT: HH:MM:SS,mmm."""
    if seconds < 0:
        seconds = 0.0
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        secs += 1
        millis = 0
    if secs >= 60:
        mins += 1
        secs = 0
    if mins >= 60:
        hrs += 1
        mins = 0
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    """Convierte segundos flotantes a formato WebVTT: HH:MM:SS.mmm."""
    if seconds < 0:
        seconds = 0.0
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        secs += 1
        millis = 0
    if secs >= 60:
        mins += 1
        secs = 0
    if mins >= 60:
        hrs += 1
        mins = 0
    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{millis:03d}"


def split_into_dynamic_chunks(segments: list[dict], min_words: int = 3, max_words: int = 5) -> list[dict]:
    """
    Divide oraciones largas en micro-segmentos de ritmo dinámico (3 a 5 palabras por bloque)
    ideal para subtítulos verticales de CapCut/TikTok/Reels.
    Calcula los timestamps proporcionales según la longitud de cada palabra.
    """
    dynamic_segments = []
    seg_counter = 0

    for seg in segments:
        text = str(seg.get("text", "")).strip()
        start = float(seg.get("start", 0.0))
        end = float(seg.get("end", 0.0))
        duration = max(0.2, end - start)

        if not text:
            continue

        words = text.split()
        if len(words) <= max_words:
            dynamic_segments.append({
                "id": seg_counter,
                "start": round(start, 3),
                "end": round(end, 3),
                "text": text
            })
            seg_counter += 1
            continue

        # Dividir palabras en grupos de min_words a max_words
        chunks = []
        i = 0
        while i < len(words):
            remaining = len(words) - i
            # Si lo que sobra es menor que min_words, anexarlo al grupo anterior si existe
            if remaining < min_words and chunks:
                chunks[-1].extend(words[i:])
                break
            # Tomar entre min_words y max_words
            take = min(max_words, remaining)
            chunks.append(words[i:i + take])
            i += take

        total_chars = sum(len(" ".join(c)) for c in chunks) or 1
        current_start = start

        for chunk_words in chunks:
            chunk_text = " ".join(chunk_words)
            chunk_weight = len(chunk_text) / total_chars
            chunk_dur = duration * chunk_weight
            chunk_end = current_start + chunk_dur

            dynamic_segments.append({
                "id": seg_counter,
                "start": round(current_start, 3),
                "end": round(min(chunk_end, end), 3),
                "text": chunk_text
            })
            seg_counter += 1
            current_start = chunk_end

    return dynamic_segments


class MediaCutter:
    """Clase para manipulación de medios y exportación de subtítulos sincronizados."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or OUTPUT_DIR

    def to_srt(self, segments: list[dict], start_offset: float = 0.0, dynamic_rhythm: bool = False, max_words: int = 5) -> str:
        """
        Genera el contenido en formato .srt.
        """
        if dynamic_rhythm:
            processed_segments = split_into_dynamic_chunks(segments, min_words=3, max_words=max_words)
        else:
            processed_segments = segments

        lines = []
        idx = 1
        for seg in processed_segments:
            text = str(seg.get("text", "")).strip()
            if not text:
                continue

            start = max(0.0, float(seg.get("start", 0.0)) - start_offset)
            end = max(start + 0.1, float(seg.get("end", 0.0)) - start_offset)

            start_str = format_timestamp_srt(start)
            end_str = format_timestamp_srt(end)

            lines.append(f"{idx}")
            lines.append(f"{start_str} --> {end_str}")
            lines.append(text)
            lines.append("")
            idx += 1

        return "\n".join(lines)

    def to_vtt(self, segments: list[dict], start_offset: float = 0.0, dynamic_rhythm: bool = False, max_words: int = 5) -> str:
        """
        Genera el contenido en formato WebVTT (.vtt).
        """
        if dynamic_rhythm:
            processed_segments = split_into_dynamic_chunks(segments, min_words=3, max_words=max_words)
        else:
            processed_segments = segments

        lines = ["WEBVTT", ""]
        idx = 1
        for seg in processed_segments:
            text = str(seg.get("text", "")).strip()
            if not text:
                continue

            start = max(0.0, float(seg.get("start", 0.0)) - start_offset)
            end = max(start + 0.1, float(seg.get("end", 0.0)) - start_offset)

            start_str = format_timestamp_vtt(start)
            end_str = format_timestamp_vtt(end)

            lines.append(f"{idx}")
            lines.append(f"{start_str} --> {end_str}")
            lines.append(text)
            lines.append("")
            idx += 1

        return "\n".join(lines)

    def save_subtitles(
        self,
        segments: list[dict],
        proyecto: str = "general",
        nombre: str = "subtitulos",
        formats: list[str] = None,
        dynamic_rhythm: bool = False,
        extra_dest_dir: str = None
    ) -> dict:
        """
        Guarda los subtítulos en disco y retorna las rutas de los archivos creados.
        """
        if formats is None:
            formats = ["srt", "vtt", "txt"]

        dest_dir = self.output_dir / proyecto / "subtitulos"
        dest_dir.mkdir(parents=True, exist_ok=True)

        results = {}

        # Generar contenido
        srt_content = self.to_srt(segments, dynamic_rhythm=dynamic_rhythm)
        vtt_content = self.to_vtt(segments, dynamic_rhythm=dynamic_rhythm)
        txt_content = "\n".join(f"[{format_timestamp_srt(s['start'])}] {s['text']}" for s in segments if s.get("text"))

        if "srt" in formats:
            srt_path = dest_dir / f"{nombre}.srt"
            srt_path.write_text(srt_content, encoding="utf-8")
            results["srt"] = str(srt_path)

            if extra_dest_dir:
                extra_path = Path(extra_dest_dir) / f"{nombre}.srt"
                extra_path.write_text(srt_content, encoding="utf-8")
                results["srt_extra"] = str(extra_path)

        if "vtt" in formats:
            vtt_path = dest_dir / f"{nombre}.vtt"
            vtt_path.write_text(vtt_content, encoding="utf-8")
            results["vtt"] = str(vtt_path)

            if extra_dest_dir:
                extra_path = Path(extra_dest_dir) / f"{nombre}.vtt"
                extra_path.write_text(vtt_content, encoding="utf-8")
                results["vtt_extra"] = str(extra_path)

        if "txt" in formats:
            txt_path = dest_dir / f"{nombre}.txt"
            txt_path.write_text(txt_content, encoding="utf-8")
            results["txt"] = str(txt_path)

        return results

    def cut_video(
        self,
        source_path: str,
        start_sec: float,
        end_sec: float,
        proyecto: str = "general",
        nombre: str = None
    ) -> dict:
        """
        Corta un fragmento de video sin re-encodear (-c copy).
        """
        if not check_ffmpeg():
            raise RuntimeError("FFmpeg no disponible.")

        src = Path(source_path).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Archivo fuente no encontrado: {source_path}")

        dest_dir = self.output_dir / proyecto / "clips"
        dest_dir.mkdir(parents=True, exist_ok=True)

        if not nombre:
            nombre = f"clip_{int(start_sec)}_{int(end_sec)}"
        output_file = dest_dir / f"{nombre}.mp4"

        duration = max(0.1, end_sec - start_sec)
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start_sec),
            "-to", str(end_sec),
            "-i", str(src),
            "-c", "copy",
            str(output_file)
        ]

        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Error al cortar video:\n{proc.stderr}")

        info = get_audio_info(str(output_file))
        return {
            "path": str(output_file),
            "duration": round(duration, 2),
            "size_mb": round(os.path.getsize(output_file) / (1024 * 1024), 2)
        }

    def extract_audio(
        self,
        source_path: str,
        start_sec: float = 0.0,
        end_sec: float = None,
        proyecto: str = "general",
        nombre: str = "audio_clip",
        normalize: bool = True,
        remove_silence: bool = False
    ) -> dict:
        """
        Extrae y opcionalmente normaliza (-16 LUFS) una pista de audio en .mp3.
        """
        if not check_ffmpeg():
            raise RuntimeError("FFmpeg no disponible.")

        src = Path(source_path).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Archivo fuente no encontrado: {source_path}")

        dest_dir = self.output_dir / proyecto / "audio"
        dest_dir.mkdir(parents=True, exist_ok=True)

        output_file = dest_dir / f"{nombre}.mp3"

        filters = []
        if normalize:
            filters.append("loudnorm=I=-16:TP=-1.5:LRA=11")
        if remove_silence:
            filters.append("silenceremove=stop_periods=-1:stop_duration=2:stop_threshold=-50dB")

        cmd = ["ffmpeg", "-y", "-ss", str(start_sec)]
        if end_sec is not None:
            cmd.extend(["-to", str(end_sec)])
        cmd.extend(["-i", str(src)])

        if filters:
            cmd.extend(["-af", ",".join(filters)])

        cmd.extend(["-vn", "-acodec", "libmp3lame", "-b:a", "192k", str(output_file)])

        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Error al extraer audio con FFmpeg:\n{proc.stderr}")

        info = get_audio_info(str(output_file))
        return {
            "path": str(output_file),
            "duration": info["duration"],
            "size_mb": round(os.path.getsize(output_file) / (1024 * 1024), 2)
        }
