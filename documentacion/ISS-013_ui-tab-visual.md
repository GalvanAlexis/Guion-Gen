# ISS-013 — UI Pestaña 3: VISUAL

**Estado:** `completado`
**Sesión:** 3
**Prioridad:** Alta
**Dependencias:** ISS-009, ISS-011, ISS-012
**Branch:** `feature/ISS-013_ui-tab-visual`

---

## Descripción

Implementar la pestaña VISUAL completa: permite configurar y generar carruseles
e imágenes a partir del guion generado en la pestaña anterior. Ofrece el toggle
entre "Modo CSS Rápido" y "Modo IA Creativa", vista previa de slides y descarga.

## Criterios de Aceptación

- [x] Toggle visible entre "CSS Rápido" e "IA Creativa" con descripción de cada modo
- [x] Selector de plantilla CSS: lla_dark, alerta_roja, estadistica
- [x] Selector de formato: 4:5 (IG/Carrusel), 9:16 (Stories/Reels), 1:1 (Post cuadrado)
- [x] Preview de slides generados en una fila horizontal desplazable
- [x] Botón "Regenerar slide X" para re-generar un slide individual sin rehacer todo
- [x] Indicador de costo estimado visible en "Modo IA" antes de generar
- [x] Barra de progreso con estado por slide: "Generando slide 3/5..."
- [x] Botón "Descargar slide X" para descarga individual
- [x] Botón "Descargar todo (ZIP)" para descarga del carrusel completo
- [x] Texto editable de cada slide antes de renderizar (para ajustes manuales)


## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [MODIFY] `src/ui/tab_visual.py` (reemplaza placeholder)
- [MODIFY] `src/ui/components.py` (agrega componente de preview de slides)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido renderizar más de 10 slides sin confirmación del usuario
- Prohibido mostrar el path del sistema de archivos al usuario
- Prohibido bloquear la UI durante el renderizado (progreso por slide)

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.ui.tab_visual import render_tab
print('OK: tab_visual importa sin errores')
"
```

---

## Flujo UX de la Pestaña

```
┌────────────────────────────────────────────────────────────┐
│  VISUAL — Generador de Carruseles                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Modo:  [CSS Rápido ●]  [IA Creativa ○]                  │
│         ~5s/slide            ~25s/slide + API cost         │
│                                                            │
│  Plantilla:   [lla_dark ▼]                                │
│  Formato:     [4:5 — Instagram] [9:16 — Stories] [1:1]   │
│                                                            │
│  Slides a generar (5):                                     │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Slide 1 — Gancho                                   │   │
│  │ Título: [¿Sabías que heredamos un déficit del 5%?] │   │
│  │ Cuerpo: [Campo editable]                           │   │
│  ├────────────────────────────────────────────────────┤   │
│  │ Slide 2 — Problema       [...]                     │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  [ GENERAR CARRUSEL ]                                      │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  PREVIEW                                                   │
│                                                            │
│  [Slide 1] [Slide 2] [Slide 3] [Slide 4] [Slide 5]       │
│  [↓ PNG]   [↓ PNG]   [↓ PNG]   [↓ PNG]   [↓ PNG]        │
│                                                            │
│  [ Descargar todo (ZIP) ]                                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```
