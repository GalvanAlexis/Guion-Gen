import json
import os
import subprocess
from pathlib import Path

class RemotionEngine:
    def export_props(self, data: dict, dest_path: str) -> str:
        """Guarda el diccionario recibido en un archivo JSON."""
        dest_path_obj = Path(dest_path)
        dest_path_obj.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path_obj, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(dest_path_obj)

    def render_video(self, props_path: str, output_path: str, project_dir: str = "./remotion") -> dict:
        """Ejecuta npx remotion render para compilar el video con las props dadas."""
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        command = f'npx remotion render src/index.ts MiVideo "{output_path}" --props="{props_path}"'
        
        try:
            # shell=True es requerido para ejecutar npx en Windows de manera confiable
            result = subprocess.run(
                command, 
                cwd=project_dir, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Error al renderizar Remotion:\n{result.stderr}")
                
            return {
                "path": str(output_path_obj),
                "status": "success",
                "stdout": result.stdout
            }
        except Exception as e:
            raise RuntimeError(f"Error al ejecutar Remotion CLI: {str(e)}")
