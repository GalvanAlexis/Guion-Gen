"""Gestor centralizado de APIs con rotación automática, balanceo y failover entre Gemini y Groq."""
import os
import re
import json
import time
from src.config.settings import GOOGLE_GEMINI_API_KEY, GROQ_API_KEY, MODELS

class APIManager:
    """Gestor de llamadas a LLMs con rotación y tolerancia a fallos."""

    def __init__(self):
        self.session_tokens = 0
        self.session_calls = 0
        self.last_provider_used = None

    def _get_groq_client(self):
        """Retorna cliente de Groq si la key está configurada."""
        key = os.getenv("GROQ_API_KEY", GROQ_API_KEY)
        if not key:
            return None
        from groq import Groq
        return Groq(api_key=key)

    def _get_gemini_client(self):
        """Retorna cliente de Google GenAI si la key está configurada."""
        key = os.getenv("GOOGLE_GEMINI_API_KEY", GOOGLE_GEMINI_API_KEY)
        if not key or not key.startswith("AIzaSy"):
            return None
        try:
            from google import genai
            return genai.Client(api_key=key)
        except Exception:
            return None

    def get_status(self) -> dict:
        """Retorna el estado de conexión y disponibilidad de cada proveedor."""
        groq_available = bool(os.getenv("GROQ_API_KEY", GROQ_API_KEY))
        gemini_key = os.getenv("GOOGLE_GEMINI_API_KEY", GOOGLE_GEMINI_API_KEY)
        gemini_available = bool(gemini_key and gemini_key.startswith("AIzaSy"))

        active_provider = "groq" if groq_available else ("gemini" if gemini_available else "none")

        return {
            "gemini": {
                "available": gemini_available,
                "model": MODELS["gemini"]["text"]
            },
            "groq": {
                "available": groq_available,
                "model": MODELS["groq"]["text"]
            },
            "active_provider": active_provider,
            "session_tokens": self.session_tokens,
            "session_calls": self.session_calls
        }

    def _call_groq(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 4096) -> dict:
        """Ejecuta inferencia a través de Groq (LLaMA 3.3 70B)."""
        client = self._get_groq_client()
        if not client:
            raise ValueError("GROQ_API_KEY no disponible o inválida.")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        model = MODELS["groq"]["text"]
        start_time = time.time()

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        elapsed = round(time.time() - start_time, 2)
        text = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else len(text.split())

        return {
            "text": text.strip(),
            "provider": "groq",
            "model": model,
            "tokens_used": tokens,
            "latency_seconds": elapsed
        }

    def _call_gemini(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 4096) -> dict:
        """Ejecuta inferencia a través de Google Gemini Flash."""
        client = self._get_gemini_client()
        if not client:
            raise ValueError("GOOGLE_GEMINI_API_KEY no disponible o requiere formato AIzaSy.")

        model = MODELS["gemini"]["text"]
        start_time = time.time()

        full_prompt = f"Instrucciones del sistema:\n{system_prompt}\n\nTarea:\n{prompt}" if system_prompt else prompt

        response = client.models.generate_content(
            model=model,
            contents=full_prompt,
        )

        elapsed = round(time.time() - start_time, 2)
        text = response.text or ""
        tokens = len(text.split()) * 2

        return {
            "text": text.strip(),
            "provider": "gemini",
            "model": model,
            "tokens_used": tokens,
            "latency_seconds": elapsed
        }

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        preferred_provider: str = "auto"
    ) -> dict:
        """
        Genera contenido con rotación y failover automático entre Groq y Gemini.
        """
        status = self.get_status()
        errors = []

        # Orden de prioridad según configuración y disponibilidad
        if preferred_provider == "gemini" and status["gemini"]["available"]:
            providers = ["gemini", "groq"]
        else:
            # Por defecto Groq es primario por cuota y velocidad
            providers = ["groq", "gemini"] if status["groq"]["available"] else ["gemini", "groq"]

        for prov in providers:
            try:
                if prov == "groq" and status["groq"]["available"]:
                    result = self._call_groq(prompt, system_prompt, temperature, max_tokens)
                    self.session_tokens += result["tokens_used"]
                    self.session_calls += 1
                    self.last_provider_used = "groq"
                    return result

                elif prov == "gemini" and status["gemini"]["available"]:
                    result = self._call_gemini(prompt, system_prompt, temperature, max_tokens)
                    self.session_tokens += result["tokens_used"]
                    self.session_calls += 1
                    self.last_provider_used = "gemini"
                    return result

            except Exception as e:
                errors.append(f"Proveedor '{prov}' falló: {str(e)}")
                continue

        raise RuntimeError(f"Todos los proveedores de LLM fallaron. Detalles:\n" + "\n".join(errors))

    def generate_json(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.5,
        max_tokens: int = 4096
    ) -> dict:
        """
        Genera y parsea una respuesta en formato JSON de forma determinista y robusta.
        """
        json_system = (
            system_prompt + "\n\nIMPORTANTE: Tu respuesta DEBE ser ÚNICAMENTE un objeto JSON válido. "
            "No incluyas explicaciones, comentarios ni texto fuera del bloque JSON."
        )

        res = self.generate(
            prompt=prompt,
            system_prompt=json_system,
            temperature=temperature,
            max_tokens=max_tokens
        )

        raw_text = res["text"]
        
        # Eliminar posibles bloques de markdown ```json ... ```
        clean_json = raw_text.strip()
        if clean_json.startswith("```"):
            clean_json = re.sub(r"^```(?:json)?\s*", "", clean_json)
            clean_json = re.sub(r"\s*```$", "", clean_json)

        # Buscar el primer '{' y el último '}' si hay texto residual
        start_idx = clean_json.find("{")
        end_idx = clean_json.rfind("}")
        
        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            clean_json = clean_json[start_idx:end_idx + 1]

        try:
            parsed_data = json.loads(clean_json)
            res["data"] = parsed_data
            return res
        except json.JSONDecodeError as err:
            raise ValueError(f"Error parseando JSON devuelto por el modelo ({res['provider']}): {str(err)}\nTexto recibido:\n{raw_text}")

# Instancia singleton global
api_manager = APIManager()
