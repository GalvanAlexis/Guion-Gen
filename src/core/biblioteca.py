"""Sistema de Biblioteca, Historial y Gestión Centralizada de Proyectos."""
import os
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from src.config.settings import OUTPUT_DIR
from src.core.script_generator import slugify


class Biblioteca:
    """Gestor de indexación, búsqueda, exportación y persistencia de proyectos."""

    def __init__(self, index_path: Path = None, base_output_dir: Path = None):
        self.output_dir = Path(base_output_dir or OUTPUT_DIR).resolve()
        self.index_path = Path(index_path or (self.output_dir / "biblioteca.json")).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._load_index()

    def _load_index(self):
        """Carga el índice JSON o lo inicializa si no existe o está corrupto."""
        if not self.index_path.exists():
            self.data = {"version": "1.0", "proyectos": []}
            self._save()
        else:
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                if not isinstance(self.data, dict) or "proyectos" not in self.data:
                    self.data = {"version": "1.0", "proyectos": []}
                    self._save()
            except (json.JSONDecodeError, OSError):
                self.data = {"version": "1.0", "proyectos": []}
                self._save()

    def _save(self):
        """Persiste el índice en disco en formato JSON indentado."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _discover_project_files(self, project_id: str) -> dict:
        """Escanea el directorio del proyecto y clasifica los artefactos generados."""
        proj_dir = self.output_dir / project_id
        if not proj_dir.exists() or not proj_dir.is_dir():
            return {"transcripcion": None, "guiones": [], "carrusel": [], "clips": [], "subtitulos": []}

        discovered = {
            "transcripcion": None,
            "guiones": [],
            "carrusel": [],
            "clips": [],
            "subtitulos": []
        }

        # 1. Transcripción y Guiones en la raíz del proyecto
        for f in proj_dir.glob("*.md"):
            rel_path = str(f.relative_to(self.output_dir)).replace("\\", "/")
            if "transcripcion" in f.name.lower():
                discovered["transcripcion"] = rel_path
            else:
                discovered["guiones"].append(rel_path)

        # 2. Carpeta guiones si existe
        guiones_dir = proj_dir / "guiones"
        if guiones_dir.exists():
            for f in guiones_dir.glob("*.md"):
                rel_path = str(f.relative_to(self.output_dir)).replace("\\", "/")
                if rel_path not in discovered["guiones"]:
                    discovered["guiones"].append(rel_path)

        # 3. Carpeta carrusel
        carrusel_dir = proj_dir / "carrusel"
        if carrusel_dir.exists():
            for f in sorted(carrusel_dir.glob("*.png")):
                discovered["carrusel"].append(str(f.relative_to(self.output_dir)).replace("\\", "/"))

        # 4. Carpeta clips
        clips_dir = proj_dir / "clips"
        if clips_dir.exists():
            for f in sorted(clips_dir.glob("*.mp4")):
                discovered["clips"].append(str(f.relative_to(self.output_dir)).replace("\\", "/"))

        # 5. Carpeta subtitulos
        sub_dir = proj_dir / "subtitulos"
        if sub_dir.exists():
            for f in sorted(sub_dir.glob("*.*")):
                if f.suffix.lower() in [".srt", ".vtt", ".txt"]:
                    discovered["subtitulos"].append(str(f.relative_to(self.output_dir)).replace("\\", "/"))

        return discovered

    def registrar(
        self,
        nombre: str,
        red: str = "general",
        tono: str = "general",
        tema: str = "",
        etiquetas: list[str] = None,
        archivos: dict | list = None,
        stats: dict = None,
        project_id: str = None
    ) -> dict:
        """
        Registra un proyecto nuevo o actualiza uno existente en el índice.
        """
        self._load_index()
        p_id = project_id or slugify(nombre)
        if not p_id:
            p_id = f"proyecto_{int(datetime.now().timestamp())}"

        discovered = self._discover_project_files(p_id)

        # Normalizar estructura de archivos
        if isinstance(archivos, dict):
            for k, v in archivos.items():
                if k in discovered:
                    if isinstance(v, list):
                        discovered[k].extend([item for item in v if item not in discovered[k]])
                    elif v and v not in discovered.get(k, []):
                        discovered[k] = v
        elif isinstance(archivos, list):
            for item in archivos:
                rel = str(item).replace("\\", "/")
                if rel.endswith(".png"):
                    discovered["carrusel"].append(rel)
                elif rel.endswith(".mp4"):
                    discovered["clips"].append(rel)
                elif rel.endswith(".srt") or rel.endswith(".vtt"):
                    discovered["subtitulos"].append(rel)
                elif "transcripcion" in rel.lower():
                    discovered["transcripcion"] = rel
                elif rel.endswith(".md"):
                    discovered["guiones"].append(rel)

        # Buscar si ya existe
        existing = next((p for p in self.data["proyectos"] if p["id"] == p_id), None)
        timestamp_iso = datetime.now().isoformat()

        if existing:
            existing["nombre"] = nombre
            existing["fecha"] = timestamp_iso
            existing["red"] = red
            existing["tono"] = tono
            existing["tema"] = tema
            if etiquetas is not None:
                existing["etiquetas"] = list(set(etiquetas))
            existing["archivos"] = discovered
            if stats:
                existing["stats"].update(stats)
            proj_record = existing
        else:
            proj_record = {
                "id": p_id,
                "nombre": nombre,
                "fecha": timestamp_iso,
                "red": red,
                "tono": tono,
                "tema": tema,
                "etiquetas": list(set(etiquetas or ["LLA", "Chascomús"])),
                "archivos": discovered,
                "stats": stats or {
                    "palabras": 0,
                    "duracion_audio": 0.0,
                    "motor_transcripcion": "groq/whisper-large-v3",
                    "tokens_usados": 0
                }
            }
            self.data["proyectos"].insert(0, proj_record)

        self._save()
        return proj_record

    def listar(self, sort_by: str = "fecha", reverse: bool = True) -> list[dict]:
        """Retorna la lista de todos los proyectos registrados."""
        self._load_index()
        projs = list(self.data["proyectos"])
        if sort_by in ["fecha", "nombre", "red", "tema"]:
            projs.sort(key=lambda x: str(x.get(sort_by, "")), reverse=reverse)
        return projs

    def obtener(self, project_id: str) -> dict | None:
        """Obtiene un proyecto por su ID."""
        self._load_index()
        return next((p for p in self.data["proyectos"] if p["id"] == project_id), None)

    def buscar(self, query: str = "", etiqueta: str = "", red: str = "") -> list[dict]:
        """Filtra proyectos según consulta textual, etiqueta o red social."""
        self._load_index()
        q_norm = query.lower().strip() if query else ""
        tag_norm = etiqueta.lower().strip() if etiqueta else ""
        red_norm = red.lower().strip() if red else ""

        results = []
        for p in self.data["proyectos"]:
            # Filtro por red
            if red_norm and p.get("red", "").lower() != red_norm:
                continue

            # Filtro por etiqueta
            if tag_norm:
                p_tags = [t.lower() for t in p.get("etiquetas", [])]
                if not any(tag_norm in t for t in p_tags):
                    continue

            # Filtro por texto en nombre, tema o id
            if q_norm:
                match_name = q_norm in p.get("nombre", "").lower()
                match_tema = q_norm in p.get("tema", "").lower()
                match_id = q_norm in p.get("id", "").lower()
                match_tag = any(q_norm in t.lower() for t in p.get("etiquetas", []))
                if not (match_name or match_tema or match_id or match_tag):
                    continue

            results.append(p)

        return results

    def eliminar(self, project_id: str, delete_files: bool = False) -> bool:
        """
        Elimina un proyecto del índice y opcionalmente borra sus archivos en disco.
        """
        self._load_index()
        idx_to_remove = None
        for i, p in enumerate(self.data["proyectos"]):
            if p["id"] == project_id:
                idx_to_remove = i
                break

        if idx_to_remove is None:
            return False

        self.data["proyectos"].pop(idx_to_remove)
        self._save()

        if delete_files:
            target_dir = self.output_dir / project_id
            if target_dir.exists() and target_dir.is_dir():
                shutil.rmtree(target_dir, ignore_errors=True)

        return True

    def exportar_zip(self, project_id: str, dest_zip_path: str = None) -> str:
        """
        Empaqueta todos los artefactos de un proyecto en un archivo .ZIP listo para descarga.
        """
        proj_dir = self.output_dir / project_id
        if not proj_dir.exists() or not proj_dir.is_dir():
            raise FileNotFoundError(f"Directorio de proyecto no encontrado: {proj_dir}")

        if dest_zip_path:
            zip_file = Path(dest_zip_path).resolve()
        else:
            zip_file = proj_dir / f"bundle_{project_id}.zip"

        zip_file.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in proj_dir.rglob("*"):
                # Evitar incluir el propio zip dentro del zip
                if file_path.is_file() and file_path != zip_file:
                    arcname = file_path.relative_to(proj_dir)
                    zipf.write(file_path, arcname=arcname)

        return str(zip_file)


# Instancia singleton global
biblioteca = Biblioteca()
