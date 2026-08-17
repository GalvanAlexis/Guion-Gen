# Guion-Gen — Índice de Issues

> Fábrica de contenido político para LLA Chascomus / Milei / Redes sociales
> Hardware: AMD Ryzen 5 5500 | 8GB RAM | Sin CUDA | Windows 11
> APIs: Gemini Flash + Groq (rotación automática)

---

## Sesión 1 — Entorno Base y Motor de Transcripción

| Issue | Título | Estado | Prioridad |
|---|---|---|---|
| [ISS-001](./ISS-001_setup-entorno-base.md) | Setup del entorno base (FFmpeg, Python, estructura) | `completado` | Alta |
| [ISS-002](./ISS-002_motor-transcripcion-dual.md) | Motor de transcripción dual (Groq Whisper → faster-whisper) | `completado` | Alta |
| [ISS-003](./ISS-003_audio-extractor.md) | Audio Extractor (FFmpeg + yt-dlp) | `completado` | Alta |
| [ISS-004](./ISS-004_markdown-builder.md) | Markdown Builder (exportación .md estructurado) | `completado` | Alta |
| [ISS-005](./ISS-005_ui-tab-fuente.md) | UI Pestaña 1 — FUENTE (ingesta y transcripción) | `completado` | Alta |

## Sesión 2 — Fábrica de Guiones

| Issue | Título | Estado | Prioridad |
|---|---|---|---|
| [ISS-006](./ISS-006_api-manager.md) | API Manager (rotación Gemini/Groq + failover) | `completado` | Alta |
| [ISS-007](./ISS-007_prompts-especializados.md) | Prompts especializados por red social | `completado` | Alta |
| [ISS-008](./ISS-008_script-generator.md) | Script Generator (orquestador de guiones) | `completado` | Alta |
| [ISS-009](./ISS-009_ui-tab-guion.md) | UI Pestaña 2 — GUION (fábrica de guiones) | `completado` | Alta |

## Sesión 3 — Motor Visual y Carruseles

| Issue | Título | Estado | Prioridad |
|---|---|---|---|
| [ISS-010](./ISS-010_plantillas-css-lla.md) | Plantillas CSS LLA (lla_dark, alerta_roja, estadistica) | `pendiente` | Alta |
| [ISS-011](./ISS-011_css-renderer.md) | CSS Renderer (HTML → Playwright → PNG) | `pendiente` | Alta |
| [ISS-012](./ISS-012_ai-renderer.md) | AI Renderer (fondos generados por Gemini Imagen) | `pendiente` | Media |
| [ISS-013](./ISS-013_ui-tab-visual.md) | UI Pestaña 3 — VISUAL (generador de carruseles) | `pendiente` | Alta |

## Sesión 4 — Media y Biblioteca

| Issue | Título | Estado | Prioridad |
|---|---|---|---|
| [ISS-014](./ISS-014_media-cutter.md) | Media Cutter (clips .mp4, subtítulos .srt/.vtt) | `pendiente` | Alta |
| [ISS-015](./ISS-015_ui-tab-media.md) | UI Pestaña 4 — MEDIA (cortador de clips) | `pendiente` | Alta |
| [ISS-016](./ISS-016_biblioteca-historial.md) | Sistema de Biblioteca e Historial | `pendiente` | Media |
| [ISS-017](./ISS-017_ui-tab-biblioteca.md) | UI Pestaña 5 — BIBLIOTECA (gestión de proyectos) | `pendiente` | Media |

## Transversal

| Issue | Título | Estado | Prioridad |
|---|---|---|---|
| [ISS-018](./ISS-018_perfil-marca-lla.md) | Perfil de marca LLA Chascomus (clients/lla_chascomus.json) | `completado` | Alta |

---

## Leyenda de Estados

- `pendiente` — No iniciado
- `en-progreso` — En desarrollo activo
- `completado` — Implementado y verificado
- `bloqueado` — Requiere dependencia externa

## Branch Naming Convention

```
feature/ISS-001_setup-entorno-base
feature/ISS-002_motor-transcripcion-dual
fix/ISS-XXX_descripcion-del-bug
```
