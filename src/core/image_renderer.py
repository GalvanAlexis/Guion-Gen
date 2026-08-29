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
        slide_data: dict = None,
        estilo: dict = None,
        force_fallback: bool = False
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

        if force_fallback:
            return self._fallback_render(index, dest_path, width, height, slide_data, estilo, full_prompt)

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
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str or "resource_exhausted" in err_str:
                # Disparar fallback local si hay error de cuota
                return self._fallback_render(index, dest_path, width, height, slide_data, estilo, full_prompt, err_msg=str(e))
                
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

    def _fallback_render(self, index, dest_path, width, height, slide_data, estilo, prompt_usado, err_msg=None):
        """Renderiza una card de alta calidad usando Playwright (sin usar API)."""
        start = time.time()
        try:
            from playwright.sync_api import sync_playwright
            
            slide_data = slide_data or {}
            estilo = estilo or {}
            
            titulo = slide_data.get("Titulo", slide_data.get("Título", f"Lamina {index}"))
            desc = slide_data.get("Descripcion Visual", slide_data.get("Descripción Visual", ""))
            dato = slide_data.get("Dato / Metrica Clave", slide_data.get("Dato / Métrica Clave", ""))
            estilo_nombre = estilo.get("nombre", "Diseño Premium")
            
            bg_color = "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)"
            text_color = "#f8fafc"
            accent_color = "#38bdf8"
            if "alerta" in estilo_nombre.lower() or "roja" in estilo_nombre.lower():
                bg_color = "linear-gradient(135deg, #450a0a 0%, #000000 100%)"
                accent_color = "#ef4444"
            elif "lla" in estilo_nombre.lower() or "libertad" in estilo_nombre.lower():
                bg_color = "linear-gradient(135deg, #020617 0%, #172554 100%)"
                accent_color = "#facc15"
                
            html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
                    body {{
                        margin: 0; padding: 0; width: {width}px; height: {height}px;
                        background: {bg_color}; color: {text_color};
                        font-family: 'Inter', sans-serif;
                        display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
                        box-sizing: border-box; padding: 80px;
                    }}
                    .container {{
                        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
                        border-radius: 40px; padding: 80px; backdrop-filter: blur(20px);
                        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); width: 100%; max-width: 900px;
                    }}
                    h1 {{ font-size: 70px; font-weight: 900; margin: 0 0 40px 0; line-height: 1.2; letter-spacing: -2px; text-wrap: balance; }}
                    p.desc {{ font-size: 40px; font-weight: 400; color: rgba(255,255,255,0.8); margin: 0 0 60px 0; line-height: 1.4; text-wrap: balance; }}
                    .dato {{
                        font-size: 50px; font-weight: 700; color: {accent_color};
                        background: rgba(0,0,0,0.3); padding: 30px 60px; border-radius: 20px; display: inline-block;
                        border-bottom: 4px solid {accent_color};
                    }}
                    .badge {{ position: absolute; top: 50px; left: 50px; font-size: 30px; font-weight: 700; color: {accent_color}; letter-spacing: 4px; text-transform: uppercase; }}
                </style>
            </head>
            <body>
                <div class="badge">{estilo_nombre}</div>
                <div class="container">
                    <h1>{titulo}</h1>
                    {f'<p class="desc">{desc}</p>' if desc else ''}
                    {f'<div class="dato">{dato}</div>' if dato else ''}
                </div>
            </body>
            </html>
            '''
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": width, "height": height})
                page.set_content(html_content)
                page.wait_for_load_state("networkidle")
                page.screenshot(path=str(dest_path))
                browser.close()
                
            return {
                "status": "fallback_success",
                "path": str(dest_path),
                "size_mb": round(dest_path.stat().st_size / (1024 * 1024), 2),
                "prompt_usado": prompt_usado,
                "index": index,
                "elapsed_sec": round(time.time() - start, 2),
                "error": err_msg
            }
        except Exception as ex:
            placeholder = self._generate_placeholder(index, str(ex), dest_path, width, height)
            return {
                "status": "error",
                "path": str(placeholder),
                "size_mb": 0.001,
                "prompt_usado": prompt_usado,
                "index": index,
                "error": f"API + Fallback failed: {str(ex)}",
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
