# ISS-009 — UI Pestaña 2: GUION

**Tipo:** `feature`
**Sesión:** 2
**Prioridad:** Alta
**Dependencias:** ISS-005, ISS-008
**Branch:** `feature/ISS-009_ui-tab-guion`

---

## Descripción

Implementar la pestaña GUION completa en Streamlit: el centro de la fábrica de
contenido donde el usuario configura los parámetros y obtiene guiones listos para
publicar en cada red social, con visualización formateada específica por plataforma.

## Criterios de Aceptación

- [x] Verifica que hay segmentos cargados (de ISS-005), si no muestra mensaje de redirección
- [x] Selector de red social con iconos: TikTok, X, Instagram, Facebook
- [x] Selector de tono: Confrontacional, Educativo, Motivacional, Urgente
- [x] Input de tema libre con sugerencias del perfil LLA Chascomus
- [x] Slider doble para seleccionar rango de la transcripción a usar
- [x] Selector de duración (solo visible para TikTok/Reels): 30s, 60s, 3min
- [x] Botón "Generar Guión" con spinner de progreso y nombre del proveedor activo
- [x] Botón "Generar 3 Variantes" para comparar opciones
- [x] Visualización formateada del resultado según la red:
  - TikTok: tabla 2 columnas VOZ / VISUAL
  - Twitter: preview de tweets con contador de caracteres
  - Instagram/Facebook: preview de slides del carrusel en secuencia
- [x] Botón "Copiar al portapapeles" para cada sección generada
- [x] Botón "Descargar .md" del guion completo
- [x] Botón "Enviar a Visual →" guarda el guion en sesión y navega a pestaña 3

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [MODIFY] `src/ui/tab_guion.py` (reemplaza placeholder)
- [MODIFY] `src/ui/components.py` (agrega renderizadores de guion por red)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido llamar APIs directamente desde la UI (usar ScriptGenerator)
- Prohibido bloquear la UI durante la generación (usar st.spinner)
- Prohibido mostrar tokens de API o información de costos al usuario

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.ui.tab_guion import render_tab
print('OK: tab_guion importa sin errores')
"
```

---

## Flujo UX de la Pestaña

```
┌────────────────────────────────────────────────────────────┐
│  GUION — Fábrica de Contenido                              │
├──────────────────────┬─────────────────────────────────────┤
│  CONFIGURACIÓN       │  RESULTADO                          │
│                      │                                     │
│  Red Social:         │  [Guion generado para TikTok]       │
│  [TikTok] [X]        │                                     │
│  [IG] [FB]           │  ┌───────────────┬───────────────┐  │
│                      │  │  VOZ EN OFF   │  VISUAL       │  │
│  Tono:               │  ├───────────────┼───────────────┤  │
│  [Confrontacional ▼] │  │ "El déficit   │ Gráfico de    │  │
│                      │  │  era del 5%"  │ barras en rojo│  │
│  Tema:               │  │               │ Texto: -5% PBI│  │
│  [________________]  │  ├───────────────┼───────────────┤  │
│                      │  │ "Hoy estamos  │ Corte a Milei │  │
│  Rango:              │  │  en superávit"│ Texto: SUPERAV│  │
│  [00:00] ←→ [15:30] │  └───────────────┴───────────────┘  │
│                      │                                     │
│  Duración: [60s ▼]   │  [Copiar] [Descargar .md]          │
│                      │  [Generar 3 Variantes]              │
│  [GENERAR GUIÓN]     │  [Enviar a Visual →]                │
│                      │                                     │
└──────────────────────┴─────────────────────────────────────┘
```

## Notas de Implementación

- Usar `st.session_state['guion_actual']` para persistir entre pestañas
- Los temas sugeridos vienen de `clients/lla_chascomus.json` → campo `temas_frecuentes`
- El preview de tweets debe mostrar el contador de caracteres (máx 280 por tweet)
- El selector de rango usa los timestamps de `st.session_state['segments']`
