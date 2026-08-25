"""Módulo para ensamblar el prompt estructurado a partir de los bloques narrativos."""

def assemble_prompt(bloques: dict, project_name: str, cliente: dict) -> str:
    """
    Ensambla el Prompt final a partir de los valores seleccionados por el usuario
    en cada bloque narrativo.
    """
    
    # Definir los nombres amigables de cada bloque
    nombres_bloques = {
        "gancho": "GANCHO",
        "problema": "PROBLEMA",
        "dato_evidencia": "DATO / EVIDENCIA",
        "contexto": "CONTEXTO",
        "responsable": "RESPONSABLE",
        "solucion": "PROPUESTA / SOLUCIÓN",
        "identidad": "IDENTIDAD POLÍTICA",
        "cierre": "CIERRE / FRASE MEMORABLE",
        "cta": "Llamado a la acción (CTA)",
        "fuente": "FUENTE"
    }
    
    # Header del prompt
    prompt_lines = [
        f"## Guion Estructurado — {project_name.replace('_', ' ').title()}\n"
    ]
    
    # Ensamblar cada bloque
    # Garantizamos el orden específico
    orden = ["gancho", "problema", "dato_evidencia", "contexto", "responsable", 
             "solucion", "identidad", "cierre", "cta", "fuente"]
             
    for key in orden:
        nombre = nombres_bloques[key]
        texto = bloques.get(key, "").strip()
        if texto:
            prompt_lines.append(f"**{nombre}:** {texto}")
        else:
            prompt_lines.append(f"**{nombre}:** *(sin definir)*")
            
    prompt_lines.append("\n---")
    
    # Footer instruccional
    nombre_cliente = cliente.get("nombre", "Genérico")
    prompt_lines.append(
        f"\nSos un redactor político experto. Usá este esquema narrativo estructurado "
        f"para generar el guion final de la publicación. Mantén la voz, estilo y valores "
        f"de '{nombre_cliente}' en todo momento."
    )
    
    return "\n".join(prompt_lines)
