# ISS-016 — Sistema de Biblioteca e Historial

**Tipo:** `feature`
**Sesión:** 4
**Prioridad:** Media
**Dependencias:** ISS-001
**Branch:** `feature/ISS-016_biblioteca-historial`

---

## Descripción

Implementar el sistema de gestión de proyectos: registro persistente de cada proyecto
creado, con sus archivos generados (transcripciones, guiones, imágenes, clips),
sistema de etiquetas y exportación de proyecto completo como ZIP.

## Criterios de Aceptación

- [ ] `biblioteca.py` mantiene un índice JSON en `output/biblioteca.json`
- [ ] Cada proyecto se registra con: nombre, fecha, red social, tono, tema, archivos generados
- [ ] Soporte de etiquetas por proyecto: "Milei", "LLA", "Chascomus", "Economía", etc.
- [ ] Función de búsqueda por nombre, fecha o etiqueta
- [ ] Exportación de proyecto completo: todos los archivos en un ZIP descargable
- [ ] Eliminación de proyecto con confirmación (borra archivos del disco)
- [ ] El índice se actualiza automáticamente al finalizar cada pipeline exitoso
- [ ] Función para cargar un proyecto anterior y restaurar su estado en sesión

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/core/biblioteca.py`
- [NEW] `output/biblioteca.json` (auto-generado en primera ejecución)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido eliminar archivos sin confirmación explícita del usuario
- Prohibido modificar archivos de proyectos ajenos al seleccionado
- Prohibido guardar API keys o datos sensibles en `biblioteca.json`

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.core.biblioteca import Biblioteca
bib = Biblioteca()
bib.registrar(
    nombre='test-proyecto',
    red='twitter',
    tono='confrontacional',
    tema='deficit fiscal',
    etiquetas=['Milei', 'LLA'],
    archivos=['output/test/transcripcion.md']
)
proyectos = bib.listar()
assert len(proyectos) >= 1, 'No se registro el proyecto'
print(f'OK: Biblioteca con {len(proyectos)} proyecto(s)')
"
```

---

## Estructura del Índice `biblioteca.json`

```json
{
  "version": "1.0",
  "proyectos": [
    {
      "id": "milei-conf-ago2026",
      "nombre": "Milei Conf AGO 2026",
      "fecha": "2026-08-16T18:00:00",
      "red": "twitter",
      "tono": "confrontacional",
      "tema": "déficit fiscal heredado",
      "etiquetas": ["Milei", "LLA", "Economía"],
      "archivos": {
        "transcripcion": "output/milei-conf-ago2026/transcripcion.md",
        "guiones": [
          "output/milei-conf-ago2026/guion_twitter_20260816.md"
        ],
        "carrusel": [
          "output/milei-conf-ago2026/carrusel/slide_01.png"
        ],
        "clips": [
          "output/milei-conf-ago2026/clips/clip_01.mp4"
        ]
      },
      "stats": {
        "palabras": 9234,
        "duracion_audio": 3012.5,
        "motor_transcripcion": "groq/whisper-large-v3",
        "tokens_usados": 4523
      }
    }
  ]
}
```
