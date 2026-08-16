# ISS-005 — UI Pestaña 1: FUENTE

**Tipo:** `feature`
**Sesión:** 1
**Prioridad:** Alta
**Dependencias:** ISS-001, ISS-002, ISS-003, ISS-004
**Branch:** `feature/ISS-005_ui-tab-fuente`

---

## Descripción

Implementar la pestaña FUENTE completa en Streamlit: la primera pantalla de trabajo
donde el usuario ingresa el contenido a procesar (video, URL o texto), lanza la
transcripción y visualiza el resultado. Es el punto de entrada al pipeline completo.

## Criterios de Aceptación

- [x] Tres modos de ingesta con selector visual: "Subir archivo", "URL YouTube", "Pegar texto"
- [x] Drag & Drop para archivos (formatos: MP4, MKV, MOV, MP3, WAV, M4A)
- [x] Input de URL con validación básica (debe comenzar con http/https)
- [x] Textarea para pegar texto directamente (bypass de transcripción)
- [x] Botón "Transcribir" que lanza el pipeline completo con spinner de progreso
- [x] Indicador de motor activo: "Usando Groq Whisper" o "Usando motor local"
- [x] Visor de transcripción con timestamps resaltados en color acento
- [x] Selector de rango de tiempo (slider doble) para visualizar subsecciones
- [x] Botón "Exportar .md" → descarga el archivo Markdown
- [x] Botón "Enviar a Guión" → guarda los segmentos en estado de sesión y navega a pestaña 2
- [x] Input de nombre de proyecto (requerido antes de transcribir)
- [x] Estadísticas visibles: duración, palabras, segmentos, motor usado, tiempo de proceso

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [MODIFY] `src/ui/tab_fuente.py` (reemplaza placeholder)
- [MODIFY] `src/ui/components.py` (agrega componentes reutilizables)
- [MODIFY] `app.py` (conecta la pestaña con el estado de sesión)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido implementar lógica de negocio en este archivo (debe llamar a los módulos core)
- Prohibido usar `st.experimental_rerun` (deprecado)
- Prohibido almacenar el audio en `st.session_state` (solo el path y los segmentos)

### 🧪 Quality Gate Determinista

```powershell
# Verificar que la pestaña carga sin errores de importación
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.ui.tab_fuente import render_tab
print('OK: tab_fuente importa sin errores')
"
```

---

## Flujo UX de la Pestaña

```
┌────────────────────────────────────────────────────────────┐
│  FUENTE — Ingesta de Contenido                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Nombre del proyecto: [________________________]           │
│                                                            │
│  ┌──────────┬──────────────┬─────────────┐               │
│  │ 📁 Subir │ 🔗 URL       │ 📝 Texto    │               │
│  └──────────┴──────────────┴─────────────┘               │
│                                                            │
│  [Zona Drag & Drop — arrastrá tu archivo acá]             │
│  Formatos: MP4, MKV, MOV, MP3, WAV, M4A (máx 500MB)      │
│                                                            │
│  Motor de transcripción:                                  │
│  ● Groq Whisper (cloud, rápido)  ○ Local (offline)        │
│                                                            │
│  [  TRANSCRIBIR  ]                                        │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  RESULTADO — Transcripción                                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  412 segmentos | 9.234 palabras | 50:23 | ⏱ 62 segundos  │
│                                                            │
│  [00:00] Buenas noches a todos los presentes...           │
│  [00:45] El déficit fiscal heredado era del 5%...         │
│  [01:23] La reforma del Estado no es una opción...        │
│  ...                                                       │
│                                                            │
│  [Exportar .md]   [Enviar a Guión →]                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Notas de Implementación

- Usar `st.session_state['segments']` para persistir entre pestañas
- Usar `st.session_state['project_name']` para el nombre del proyecto activo
- El spinner debe mostrar sub-estados: "Extrayendo audio...", "Transcribiendo...", "Formateando..."
- Colores de timestamps: `color: #8B5CF6` (violeta LLA) en la transcripción
