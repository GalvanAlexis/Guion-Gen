"""Motor de generación de fondos artísticos mediante IA (Gemini Imagen 3) con caché local y fallback."""
import os
import time
import base64
import hashlib
from pathlib import Path
from src.config.settings import TEMP_DIR, GOOGLE_GEMINI_API_KEY
from src.core.script_generator import slugify

TONE_PROMPTS = {
    "confrontacional": "dramatic, dark, high contrast, stormy political atmosphere, tension, abstract economic storm, deep shadows",
    "educativo": "clean, modern infographic backdrop, financial data flow, subtle geometric shapes, dark technology, analytical mood",
    "motivacional": "inspirational, dawn light rays, golden horizons, freedom and economic growth, uplifting modern art",
    "urgente": "red and black alarm, emergency mood, dramatic dark atmosphere, critical breaking news aesthetic, neon danger glow"
}

class AIRenderer:
    """Generador y gestor de fondos artísticos para carruseles y publicaciones."""

    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or (TEMP_DIR / "cache_bg")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.last_latency = 0.0

    def build_image_prompt(self, tema: str, tono: str = "confrontacional", formato: str = "4:5") -> str:
        """
        Construye un prompt visual abstracto y conceptual con guardrails estrictos de seguridad.
        """
        tono_norm = tono.lower().strip()
        style_tone = TONE_PROMPTS.get(tono_norm, TONE_PROMPTS["confrontacional"])
        
        format_desc = "4:5 vertical poster format" if formato == "4:5" else ("9:16 vertical full wallpaper" if formato == "9:16" else "1:1 square format")
        tema_clean = tema.strip() if tema else "economía y libertad"

        return (
            f"Concept art, Argentine economic and political theme: {tema_clean}. "
            f"Mood and style: {style_tone}, cinematic volumetric lighting, deep obsidian dark textures, {format_desc}. "
            "High resolution 8k."
        )

    def generate_background(
        self,
        tema: str,
        tono: str = "confrontacional",
        project_name: str = "general",
        formato: str = "4:5",
        use_cache: bool = True
    ) -> str | None:
        """
        Genera un fondo artístico PNG o lo recupera desde la caché local en disco.
        Si la API no está disponible o falla, retorna None de forma segura.
        """
        t0 = time.time()
        prompt = self.build_image_prompt(tema=tema, tono=tono, formato=formato)
        prompt_hash = hashlib.sha256(f"{tema}_{tono}_{formato}".encode("utf-8")).hexdigest()[:12]
        slug_tema = slugify(tema) if tema else "tema"
        cache_file = self.cache_dir / f"bg_{slug_tema}_{prompt_hash}.png"

        # 1. Verificar Caché en Disco
        if use_cache and cache_file.exists() and cache_file.stat().st_size > 1000:
            self.last_latency = round(time.time() - t0, 3)
            return str(cache_file)

        # 2. Llamada a Gemini Imagen con reintento
        key = os.getenv("GOOGLE_GEMINI_API_KEY", GOOGLE_GEMINI_API_KEY)
        if not key:
            return None

        for intento in range(2):
            try:
                from google import genai
                client = genai.Client(api_key=key)
                aspect_ratio = "3:4" if formato == "4:5" else ("9:16" if formato == "9:16" else "1:1")

                # Llamada directa al modelo
                result = client.models.generate_images(
                    model="imagen-3.0-generate-001",
                    prompt=prompt,
                    config=dict(
                        number_of_images=1,
                        aspect_ratio=aspect_ratio,
                        output_mime_type="image/png"
                    )
                )

                if result and result.generated_images:
                    image_bytes = result.generated_images[0].image.image_bytes
                    with open(cache_file, "wb") as f:
                        f.write(image_bytes)
                    self.last_latency = round(time.time() - t0, 3)
                    return str(cache_file)

            except Exception as e:
                import traceback
                print(f"[ERROR Gemini IA] Intento {intento+1} falló: {e}")
                traceback.print_exc()
                if "429" in str(e) or "404" in str(e) or intento == 1:
                    raise RuntimeError(f"Fallo en API de Gemini Imagen: {str(e)}")
                time.sleep(1.0)

        return None

    def get_background_b64(
        self,
        tema: str,
        tono: str = "confrontacional",
        project_name: str = "general",
        formato: str = "4:5",
        use_cache: bool = True
    ) -> str:
        """
        Retorna la representación Base64 del fondo generado o cadena vacía si está en modo CSS puro.
        """
        bg_path = self.generate_background(
            tema=tema,
            tono=tono,
            project_name=project_name,
            formato=formato,
            use_cache=use_cache
        )
        if bg_path and Path(bg_path).exists():
            try:
                with open(bg_path, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                return ""
        return ""

ai_renderer = AIRenderer()
