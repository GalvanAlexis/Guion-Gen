# ISS-010 — Plantillas CSS LLA (lla_dark, alerta_roja, estadistica)

**Tipo:** `feature`
**Sesión:** 3
**Prioridad:** Alta
**Dependencias:** ISS-001, ISS-018
**Branch:** `feature/ISS-010_plantillas-css-lla`

---

## Descripción

Diseñar e implementar las 3 plantillas visuales base HTML/CSS para la generación
de carruseles e imágenes de contenido político para LLA Chascomus. Las plantillas
son renderizadas por Playwright (ISS-011) para exportar PNG de alta calidad.

Cada plantilla soporta variables inyectadas por Jinja2: título, cuerpo, número
de slide, logo, URL, hashtags y paleta de colores del cliente.

## Criterios de Aceptación

- [ ] Plantilla `lla_dark`: fondo oscuro, violeta + dorado, tipografía Outfit
- [ ] Plantilla `alerta_roja`: fondo negro, rojo intenso, texto blanco, urgente
- [ ] Plantilla `estadistica`: gráficos simples CSS, tablas comparativas, datos duros
- [ ] Todas las plantillas en formato 1080x1350px (Instagram 4:5)
- [ ] Versión 9:16 (1080x1920) incluida en cada plantilla (para Stories/Reels)
- [ ] Logo del cliente inyectable en cabecera (PNG Base64 o ruta local)
- [ ] Hashtags en pie de página configurables
- [ ] Número de slide visible en la esquina (slide N / total)
- [ ] Tipografías cargadas desde Google Fonts (Outfit + Inter)
- [ ] Responsivo al viewport de Playwright (no usa px absolutos en el layout)

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/templates/lla_dark/index.html`
- [NEW] `src/templates/lla_dark/styles.css`
- [NEW] `src/templates/alerta_roja/index.html`
- [NEW] `src/templates/alerta_roja/styles.css`
- [NEW] `src/templates/estadistica/index.html`
- [NEW] `src/templates/estadistica/styles.css`
- [NEW] `src/templates/base.html` (layout base compartido con Jinja2 blocks)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido usar `px` absolutos en height del contenedor principal (usar `100vh`)
- Prohibido usar imágenes externas sin fallback local (siempre Base64 o ruta relativa)
- Prohibido JavaScript en las plantillas (deben funcionar como HTML/CSS estático puro)
- Prohibido usar colores fuera de la paleta definida en `lla_chascomus.json`

### 🧪 Quality Gate Determinista

```powershell
# Verificar que el HTML es válido y abre sin errores en el navegador
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('src/templates'))
tmpl = env.get_template('lla_dark/index.html')
html = tmpl.render(titulo='Test', cuerpo='Test body', slide_num=1, total_slides=5)
assert len(html) > 500, 'Template muy corto'
print('OK: Template lla_dark renderiza correctamente')
"
```

---

## Especificación Visual

### Paleta LLA Dark

```css
:root {
  --bg:       #0a0a10;
  --card:     rgba(255,255,255,0.04);
  --primary:  #8B5CF6;    /* Violeta LLA */
  --gold:     #F59E0B;    /* Dorado editorial */
  --text:     #F8FAFC;
  --muted:    #94A3B8;
  --border:   rgba(139,92,246,0.2);
}
```

### Variables Jinja2 Disponibles

| Variable | Tipo | Descripción |
|---|---|---|
| `titulo` | str | Título principal del slide |
| `cuerpo` | str | Texto del cuerpo (puede incluir `<br>` y listas) |
| `slide_num` | int | Número del slide actual |
| `total_slides` | int | Total de slides del carrusel |
| `logo_b64` | str | Logo del cliente en Base64 |
| `url` | str | URL del cliente |
| `hashtags` | list | Lista de hashtags para el pie |
| `tipo` | str | "gancho" / "problema" / "solucion" / "cierre" |
| `dato_destacado` | str | Número grande para estadísticas |
| `subtitulo` | str | Subtítulo opcional |
