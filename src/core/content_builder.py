"""Módulo para generar opciones de bloques narrativos usando IA."""
import json
from src.config.api_manager import api_manager

def generate_narrative_options(transcription_text: str, cliente: dict) -> dict:
    """
    Genera 3 opciones de enfoque para cada uno de los 10 bloques narrativos 
    basado en la transcripción y el perfil del cliente.
    """
    if not transcription_text or not transcription_text.strip():
        # Si no hay texto, retornar estructura vacía
        return {k: [] for k in [
            "gancho", "problema", "dato_evidencia", "contexto", 
            "responsable", "solucion", "identidad", "cierre", "cta", "fuente"
        ]}
    
    system_prompt = f"""Sos un estratega político experto en comunicación digital.
Tu tarea es analizar la transcripción proporcionada y extraer 3 opciones diferentes para cada bloque narrativo clave.
El tono debe alinearse con el cliente: {cliente.get("nombre", "Genérico")}.
Valores del cliente: {', '.join(cliente.get("valores", []))}.

Los 10 bloques son:
1. gancho: Captar atención (pregunta, dato fuerte, contraste).
2. problema: Explicar qué está pasando, una idea central.
3. dato_evidencia: Número, comparación o hecho verificable.
4. contexto: Por qué el dato importa (antes vs ahora).
5. responsable: Decisión política que causó el problema.
6. solucion: Propuesta concreta.
7. identidad: Conectar con los valores del cliente.
8. cierre: Frase corta y memorable.
9. cta: Llamado a la acción (compartir, opinar, guardar).
10. fuente: Organismo, informe o documento de donde salen los datos.

REGLA ESTRICTA: El output DEBE ser un JSON con 10 claves exactas correspondientes a los nombres de los bloques (en minúsculas y snake_case). Cada clave debe contener un array de 3 strings cortos (máx 1-2 oraciones).
Ejemplo de estructura requerida:
{{
  "gancho": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "problema": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "dato_evidencia": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "contexto": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "responsable": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "solucion": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "identidad": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "cierre": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "cta": ["Opcion 1", "Opcion 2", "Opcion 3"],
  "fuente": ["Opcion 1", "Opcion 2", "Opcion 3"]
}}"""

    prompt = f"Transcripción a analizar:\n{transcription_text}"
    
    try:
        res = api_manager.generate_json(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=4000
        )
        data = res.get("data", {})
        
        # Validar claves
        keys = ["gancho", "problema", "dato_evidencia", "contexto", "responsable", "solucion", "identidad", "cierre", "cta", "fuente"]
        for k in keys:
            if k not in data or not isinstance(data[k], list):
                data[k] = []
            # Rellenar si faltan opciones para llegar a 3
            while len(data[k]) < 3:
                data[k].append("")
            # Truncar si hay más de 3
            data[k] = data[k][:3]
            
        return data
    except Exception as e:
        print(f"Error generando opciones narrativas: {e}")
        return {k: [] for k in [
            "gancho", "problema", "dato_evidencia", "contexto", 
            "responsable", "solucion", "identidad", "cierre", "cta", "fuente"
        ]}
