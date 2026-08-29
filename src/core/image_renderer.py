"""Motor de generacion de imagenes por lamina usando Google Gemini Imagen."""
import os
import base64
import time
from pathlib import Path


class ImageRenderer:
    """
    Genera imagenes PNG para cada lamina del brief visual usando la API de Gemini.
    Soporta el modelo imagen-3.0-generate-001.
    """

    IMAGE_MODEL = "gemini-3.1-flash-image"

    def __init__(self):
        self._client = None

    def _get_client(self):
        """Inicializa el cliente de Google GenAI de forma lazy."""
        if self._client is not None:
            return self._client
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY", "")
        if not api_key or len(api_key.strip()) < 10:
            raise ValueError(
                "GOOGLE_GEMINI_API_KEY no configurada. "
                "Agregala al archivo .env del proyecto."
            )
        try:
            from google import genai
            self._client = genai.Client(api_key=api_key.strip())
            return self._client
        except ImportError:
            raise ImportError(
                "La libreria 'google-genai' no esta instalada. "
                "Ejecuta: pip install google-genai"
            )

    def render_slide(
        self,
        prompt: str,
        index: int,
        project_name: str,
        output_dir=None,
        width: int = 1080,
        height: int = 1350,
    ) -> dict:
        """
        Genera una imagen PNG para una lamina del brief.

        Args:
            prompt: Descripcion visual detallada de la lamina.
            index: Numero de lamina (1-based).
            project_name: Nombre del proyecto.
            output_dir: Directorio de salida. Si es None, usa output/<project_name>/imagenes/.
            width: Ancho de la imagen en pixeles (referencial).
            height: Alto de la imagen en pixeles (referencial).

        Returns:
            dict con keys: path, size_mb, prompt_usado, index, status
        """
        from src.config.settings import OUTPUT_DIR

        if output_dir is None:
            output_dir = OUTPUT_DIR / project_name / "imagenes"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"lamina_{index:02d}.png"
        dest_path = output_dir / filename

        # Prompt enriquecido con especificaciones tecnicas
        full_prompt = (
            f"{prompt}\n\n"
            f"Aspect ratio: {width}x{height} pixels. "
            "Photorealistic, high quality, social media ready, "
            "clean composition, professional lighting."
        )

        client = self._get_client()
        start = time.time()

        try:
            from google.genai import types as genai_types

            response = client.models.generate_content(
                model=self.IMAGE_MODEL,
                contents=full_prompt,
                config=genai_types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )

            image_data = None
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    import base64 as _b64
                    image_data = _b64.b64decode(part.inline_data.data)
                    break

            if image_data is None:
                raise RuntimeError(
                    "El modelo no devolvio una imagen. "
                    "Verifica que la API key tenga acceso al modelo de imagen."
                )

            dest_path.write_bytes(image_data)
            elapsed = round(time.time() - start, 2)
            size_mb = round(dest_path.stat().st_size / (1024 * 1024), 2)

            return {
                "status": "success",
                "path": str(dest_path),
                "size_mb": size_mb,
                "prompt_usado": full_prompt,
                "index": index,
                "elapsed_sec": elapsed,
            }

        except Exception as e:
            placeholder = self._generate_placeholder(index, str(e), dest_path, width, height)
            return {
                "status": "error",
                "path": str(placeholder),
                "size_mb": 0.001,
                "prompt_usado": full_prompt,
                "index": index,
                "error": str(e),
                "elapsed_sec": round(time.time() - start, 2),
            }

    def _generate_placeholder(self, index: int, error_msg: str, dest_path, width: int, height: int):
        """Genera un PNG placeholder cuando falla la API."""
        dest_path = Path(dest_path)
        try:
            from PIL import Image, ImageDraw
            img = Image.new("RGB", (width, height), color=(20, 20, 40))
            draw = ImageDraw.Draw(img)
            draw.text(
                (width // 2, height // 2),
                f"Lamina {index}\n(Error API)",
                fill=(200, 100, 100),
                anchor="mm",
            )
            img.save(str(dest_path), "PNG")
        except Exception:
            minimal_png = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDQADTQF8eiX3GAAAAABJRU5ErkJggg=="
            )
            dest_path.write_bytes(minimal_png)
        return dest_path

    def render_all_slides(
        self,
        items: list,
        project_name: str,
        tipo_contenido: str,
        estilo: dict,
        dimensiones: str,
        progress_callback=None,
    ) -> list:
        """
        Renderiza todas las laminas/escenas del brief.

        Args:
            items: Lista de dicts del DataFrame.
            project_name: Nombre del proyecto.
            tipo_contenido: "Imagen" o "Video".
            estilo: Dict del estilo visual seleccionado.
            dimensiones: String de dimensiones ej "4:5 (1080x1350)".
            progress_callback: callable(current, total, msg) para progreso.

        Returns:
            Lista de dicts con los resultados de cada lamina.
        """
        width, height = 1080, 1350
        if "1080x1920" in dimensiones:
            width, height = 1080, 1920
        elif "1080x1080" in dimensiones:
            width, height = 1080, 1080
        elif "1920x1080" in dimensiones:
            width, height = 1920, 1080

        estilo_nombre = estilo.get("nombre", "Editorial")
        results = []

        for i, item in enumerate(items):
            idx = i + 1
            if tipo_contenido == "Imagen":
                titulo = item.get("Titulo", item.get("Título", f"Lamina {idx}"))
                desc = item.get("Descripcion Visual", item.get("Descripción Visual", ""))
                dato = item.get("Dato / Metrica Clave", item.get("Dato / Métrica Clave", ""))
                prompt = (
                    f"Estilo visual: {estilo_nombre}. "
                    f"Titulo: '{titulo}'. "
                    f"Composicion visual: {desc}. "
                    + (f"Dato clave: {dato}." if dato else "")
                )
            else:
                desc = item.get("Descripcion Visual", item.get("Descripción Visual", ""))
                texto = item.get("Texto en Pantalla", "")
                movimiento = item.get("Movimiento de Camara", item.get("Movimiento de Cámara", ""))
                prompt = (
                    f"Estilo cinematografico: {estilo_nombre}. "
                    f"Escena: {desc}. "
                    + (f"Texto en pantalla: '{texto}'." if texto else "")
                    + (f"Camara: {movimiento}." if movimiento else "")
                )

            if progress_callback:
                progress_callback(i, len(items), f"Generando lamina {idx}/{len(items)}...")

            result = self.render_slide(
                prompt=prompt,
                index=idx,
                project_name=project_name,
                width=width,
                height=height,
            )
            results.append(result)

        if progress_callback:
            progress_callback(len(items), len(items), "Generacion completada.")

        return results
