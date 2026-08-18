# ISS-015 — UI Pestaña 4: MEDIA

**Estado:** `completado`
**Sesión:** 4
**Prioridad:** Alta
**Dependencias:** ISS-005, ISS-014
**Branch:** `feature/ISS-014-015_media-cutter-y-ui`

---

## Descripción

Implementar la pestaña MEDIA: herramienta de corte y exportación de audio/video
con timeline interactivo basado en la transcripción, para extraer clips exactos y
generar subtítulos sincronizados compatibles con CapCut y YouTube.

## Criterios de Aceptación

- [x] Timeline visual con segmentos de transcripción como marcas de tiempo
- [x] Selector de rango de corte: inputs de texto `MM:SS` + sliders de ajuste fino
- [x] Preview del texto transcripto en el rango seleccionado
- [x] Botón "Cortar clip .mp4" con spinner de progreso
- [x] Botón "Extraer audio .mp3" con opción de normalizar volumen
- [x] Botón "Generar .srt" → descarga subtítulos sincronizados del rango
- [x] Botón "Generar .vtt" → descarga subtítulos para YouTube
- [x] Toggle "Eliminar silencios largos (>2s)" antes de exportar audio
- [x] Lista de clips ya exportados en esta sesión con descarga directa
- [x] Estadísticas del corte: duración del clip, tamaño estimado del archivo


## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [MODIFY] `src/ui/tab_media.py` (reemplaza placeholder)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido procesar video sin el archivo fuente en `temp/`
- Prohibido mostrar paths del sistema al usuario
- Prohibido bloquear la UI durante el corte

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.ui.tab_media import render_tab
print('OK: tab_media importa sin errores')
"
```

---

## Flujo UX de la Pestaña

```
┌────────────────────────────────────────────────────────────┐
│  MEDIA — Corte de Clips y Subtítulos                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  TIMELINE DE TRANSCRIPCIÓN                                 │
│  ████████████████████████████████████████████ 50:23       │
│       ▲ inicio                    ▲ fin                    │
│    [05:47]                     [07:30]                     │
│                                                            │
│  Texto en rango seleccionado (01:43):                      │
│  "La reforma del Estado no es una opción, es una          │
│   obligación constitucional. El déficit..."                │
│                                                            │
│  Opciones de audio:                                        │
│  [✓] Normalizar volumen (-16 LUFS)                        │
│  [ ] Eliminar silencios (>2 seg)                          │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  [Cortar clip .mp4]  [Extraer audio .mp3]            │ │
│  │  [Generar .srt]      [Generar .vtt]                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  CLIPS EXPORTADOS EN ESTA SESIÓN                           │
│                                                            │
│  clip_01.mp4 (01:43) — 18.3 MB          [↓ Descargar]    │
│  subtitulos.srt      — 2.1 KB           [↓ Descargar]    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```
