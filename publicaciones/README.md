# Archivo de Publicaciones Terminadas — Guion-Gen

Este directorio almacena el contenido final listo para ser publicado en cada una de las redes sociales, clasificado por plataforma y con una convención de nomenclatura estandarizada.

---

## Estructura de Carpetas

```
publicaciones/
├── ig/         Contenido para Instagram (Carruseles 4:5, Stories 9:16, Copies P.A.S.C.)
│   └── .gitkeep
├── x/          Contenido para X / Twitter (Hilos de tweets, posts de opinión, resúmenes)
│   └── .gitkeep
├── fb/         Contenido para Facebook (Posts extensos, debates, adaptaciones comunitarias)
│   └── .gitkeep
├── tiktok/     Contenido para TikTok / Reels (Guiones técnicos 2 columnas, clips cortados .mp4, subtítulos .srt)
│   └── .gitkeep
└── README.md   Reglas de nomenclatura y organización
```

---

## Regla de Nomenclatura Obligatoria

Todos los archivos generados y exportados en este directorio deben seguir estrictamente el patrón:

```text
AAAA-MM-DD_red-social_titulo-tema_numero.extension
```

### Componentes de la Nomenclatura

| Componente | Formato | Descripción | Ejemplo |
|---|---|---|---|
| **Fecha** | `AAAA-MM-DD` | Fecha de creación o fecha programada de publicación | `2026-08-16` |
| **Red Social** | `ig`, `x`, `fb`, `tiktok` | Identificador de la plataforma destino en minúsculas | `ig`, `tiktok` |
| **Título/Tema** | `palabras-con-guiones` | Descripción concisa del tema en minúsculas, sin espacios ni caracteres especiales | `deficit-fiscal`, `reforma-estado` |
| **Número** | `01`, `02`, `03`... | Número correlativo de la pieza o número de diapositiva del carrusel | `01`, `slide-01` |
| **Extensión** | `.md`, `.png`, `.mp4`, `.srt` | Tipo de archivo según el medio generado | `.md`, `.png`, `.mp4` |

---

## Ejemplos Prácticos

### 1. Instagram (`publicaciones/ig/`)
- `2026-08-16_ig_deficit-fiscal_copy.md` (Copy del pie de foto con hashtags)
- `2026-08-16_ig_deficit-fiscal_slide-01.png` (Portada del carrusel)
- `2026-08-16_ig_deficit-fiscal_slide-02.png` (Slide de problema)
- `2026-08-16_ig_deficit-fiscal_carrusel-completo.zip` (Paquete ZIP descargable)

### 2. X / Twitter (`publicaciones/x/`)
- `2026-08-16_x_discurso-milei-hilo_01.md` (Hilo completo con los 8 tweets formateados)
- `2026-08-17_x_superavit-primario_01.md` (Tweet individual con dato destacado)

### 3. TikTok / Reels (`publicaciones/tiktok/`)
- `2026-08-16_tiktok_reforma-estado_guion-tecnico_01.md` (Guion 2 columnas VOZ / VISUAL)
- `2026-08-16_tiktok_reforma-estado_clip_01.mp4` (Fragmento de video cortado)
- `2026-08-16_tiktok_reforma-estado_subtitulos_01.srt` (Archivo de subtítulos sincronizados)

### 4. Facebook (`publicaciones/fb/`)
- `2026-08-16_fb_seguridad-chascomus_post_01.md` (Post argumentativo con llamado al debate local)
