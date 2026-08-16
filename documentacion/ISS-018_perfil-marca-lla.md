# ISS-018 — Perfil de Marca LLA Chascomus

**Tipo:** `chore`
**Sesión:** 1 (transversal)
**Prioridad:** Alta
**Dependencias:** ISS-001
**Branch:** `feature/ISS-018_perfil-marca-lla`

---

## Descripción

Crear el perfil de marca completo para LLA Chascomus en `clients/lla_chascomus.json`.
Este archivo es la fuente de verdad de todas las preferencias de estilo, temas
frecuentes, hashtags, plantillas de guiones y configuraciones de tono para el cliente.
Todos los módulos del sistema lo leen para personalizar el contenido generado.

## Criterios de Aceptación

- [ ] Archivo JSON válido en `clients/lla_chascomus.json`
- [ ] Paleta de colores completa (primario, secundario, fondo, texto, alerta)
- [ ] Tipografías configuradas
- [ ] Tono base y restricciones de estilo definidas (sin emojis en tono serio)
- [ ] Lista de hashtags fijos por red social
- [ ] Lista de al menos 10 temas frecuentes para el selector de la UI
- [ ] Plantillas de prompts predefinidas para cada tipo de contenido político
- [ ] Configuración de logo (nombre del archivo esperado en `clients/assets/`)
- [ ] El archivo carga correctamente desde `settings.py`

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `clients/lla_chascomus.json`
- [NEW] `clients/assets/` (carpeta para logo y assets de marca)
- [MODIFY] `src/config/settings.py` (cargar el perfil del cliente por defecto)

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido incluir información personal o datos privados en el perfil
- Prohibido hardcodear API keys en este archivo
- Prohibido usar emojis en los campos de tono "serio" y "confrontacional"

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
import json
with open('clients/lla_chascomus.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)
campos = ['nombre', 'paleta', 'tipografia', 'tono_base', 'hashtags_fijos', 'temas_frecuentes', 'plantillas']
for campo in campos:
    assert campo in perfil, f'Falta campo requerido: {campo}'
assert len(perfil['temas_frecuentes']) >= 10, 'Menos de 10 temas frecuentes'
print(f'OK: Perfil LLA Chascomus válido con {len(perfil[\"temas_frecuentes\"])} temas')
"
```

---

## Estructura Completa del Perfil

```json
{
  "id": "lla_chascomus",
  "nombre": "LLA Chascomus",
  "descripcion": "Espacio político de La Libertad Avanza en Chascomus, Buenos Aires.",
  "website": "",
  "redes": {
    "instagram": "@llachascomus",
    "tiktok": "@llachascomus",
    "twitter": "@llachascomus",
    "facebook": "LLA Chascomus"
  },
  "paleta": {
    "primario":    "#8B5CF6",
    "secundario":  "#F59E0B",
    "fondo":       "#0a0a10",
    "texto":       "#F8FAFC",
    "muted":       "#94A3B8",
    "alerta":      "#EF4444",
    "borde":       "rgba(139,92,246,0.2)"
  },
  "tipografia": {
    "titulo":  "Outfit",
    "cuerpo":  "Inter",
    "codigo":  "JetBrains Mono"
  },
  "tono_base": "serio, directo, político, sin emojis en tono confrontacional",
  "restricciones": [
    "Sin emojis en tono confrontacional y serio",
    "Sin lenguaje informal ni jerga de internet",
    "Sin superlativismo vacío (increíble, espectacular, etc.)",
    "Siempre citar la fuente del dato estadístico si se usa",
    "Nunca insultar directamente a personas, atacar ideas y gestiones"
  ],
  "hashtags_fijos": {
    "general":   ["#LLA", "#LibertadAvanza", "#Chascomus"],
    "milei":     ["#Milei", "#JavierMilei", "#LLA"],
    "local":     ["#Chascomus", "#LLAChascomus", "#BuenosAires"],
    "economia":  ["#LibertadEconómica", "#Superávit", "#AjusteFiscal"],
    "seguridad": ["#Seguridad", "#Chascomus"]
  },
  "temas_frecuentes": [
    "déficit fiscal heredado",
    "superávit primario logrado",
    "reforma del Estado",
    "inflación y sus causas",
    "libertad económica vs intervencionismo",
    "seguridad en Chascomus",
    "gestión local vs provincial",
    "kirchnerismo y sus consecuencias",
    "motosierra y ajuste del gasto público",
    "privatizaciones y empresa privada",
    "dolarización y estabilidad monetaria",
    "derechos individuales vs colectivismo",
    "corrupción en el Estado anterior",
    "reservas del Banco Central"
  ],
  "plantillas": {
    "discurso_hilo": {
      "descripcion": "Extraer las 8 frases más impactantes de un discurso en formato hilo viral para X",
      "red": "twitter",
      "tono": "confrontacional",
      "estructura": "gancho → 6 puntos argumentales → cierre con CTA"
    },
    "estadistica_pasc": {
      "descripcion": "Carrusel educativo con dato duro → problema → solución libertaria",
      "red": "instagram",
      "tono": "educativo",
      "estructura": "gancho (dato) → problema → agitación → solución → cierre"
    },
    "denuncia_urgente": {
      "descripcion": "Post de alerta con dato concreto y pregunta retórica final",
      "red": "instagram",
      "tono": "urgente",
      "estructura": "pregunta retórica → dato → contexto → llamado a la acción"
    },
    "reels_60s": {
      "descripcion": "Guion técnico 2 columnas para TikTok/Reels de 60 segundos",
      "red": "tiktok",
      "tono": "confrontacional",
      "duracion": 60,
      "estructura": "hook (0-5s) → desarrollo (5-50s) → CTA (50-60s)"
    },
    "lla_local": {
      "descripcion": "Contenido con referencias específicas a la gestión en Chascomus",
      "red": "facebook",
      "tono": "educativo",
      "estructura": "contexto local → comparativa → propuesta LLA local"
    },
    "comparativa": {
      "descripcion": "Tabla comparativa de indicadores antes/después (kirchnerismo vs Milei)",
      "red": "instagram",
      "tono": "educativo",
      "estructura": "título impactante → tabla comparativa → conclusión"
    }
  },
  "logo": {
    "archivo": "clients/assets/lla_logo.png",
    "tamano_cabecera_px": 80,
    "tamano_footer_px": 55
  }
}
```
