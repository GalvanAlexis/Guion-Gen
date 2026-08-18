# ISS-017 — UI Pestaña 5: BIBLIOTECA

**Estado:** `completado`
**Sesión:** 4
**Prioridad:** Media
**Dependencias:** ISS-016
**Branch:** `feature/ISS-017_ui-tab-biblioteca`

---

## Descripción

Implementar la pestaña BIBLIOTECA: panel de gestión de proyectos con historial
completo, búsqueda, vista detallada de cada proyecto y exportación. Es el archivo
permanente de toda la producción de contenido.

## Criterios de Aceptación

- [x] Lista de proyectos con buscador por nombre, tema o etiqueta
- [x] Cada proyecto muestra: nombre, fecha, red, tono, tema, cantidad de archivos
- [x] Expandir proyecto muestra lista de archivos con previsualización de imágenes
- [x] Botón "Cargar proyecto" restaura el estado en sesión para continuar trabajando
- [x] Botón "Descargar ZIP" exporta todo el proyecto
- [x] Botón "Eliminar" con diálogo de confirmación
- [x] Filtros por red social, etiqueta y fecha
- [x] Estadísticas globales en cabecera: total proyectos, palabras transcritas, imágenes generadas


## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [MODIFY] `src/ui/tab_biblioteca.py` (reemplaza placeholder)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido eliminar archivos sin confirmación del usuario en la UI
- Prohibido mostrar paths del sistema de archivos al usuario
- Prohibido modificar `biblioteca.json` directamente desde la UI (usar `Biblioteca` class)

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.ui.tab_biblioteca import render_tab
print('OK: tab_biblioteca importa sin errores')
"
```

---

## Flujo UX de la Pestaña

```
┌────────────────────────────────────────────────────────────┐
│  BIBLIOTECA — Historial de Proyectos                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  3 proyectos | 24.891 palabras | 15 imágenes | 4 clips    │
│                                                            │
│  [Buscar...] [Todas las redes ▼] [Todas las etiquetas ▼] │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ▶ Milei Conf AGO 2026                                    │
│    Twitter | Confrontacional | "déficit fiscal"            │
│    16 ago 2026 | 9.234 palabras | 1 guion | 5 imágenes   │
│    #Milei #LLA #Economía                                   │
│    [Cargar] [↓ ZIP] [Eliminar]                            │
│                                                            │
│  ▶ LLA Chascomus — Seguridad                              │
│    Instagram | Urgente | "inseguridad local"               │
│    14 ago 2026 | 4.120 palabras | 2 guiones | 10 imágenes │
│    [Cargar] [↓ ZIP] [Eliminar]                            │
│                                                            │
│  ▶ Debate TV — Resumen                                    │
│    TikTok | Educativo | "reforma del Estado"              │
│    12 ago 2026 | 11.547 palabras | 3 clips | 0 imágenes  │
│    [Cargar] [↓ ZIP] [Eliminar]                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```
