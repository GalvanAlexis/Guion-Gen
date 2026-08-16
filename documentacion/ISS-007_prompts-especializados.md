# ISS-007 — Prompts Especializados por Red Social

**Tipo:** `feature`
**Sesión:** 2
**Prioridad:** Alta
**Dependencias:** ISS-004, ISS-006
**Branch:** `feature/ISS-007_prompts-especializados`

---

## Descripción

Crear el sistema de prompts especializados para la generación de guiones y copys
adaptados a cada red social. Cada módulo de prompts encapsula el system prompt,
el formato de salida esperado y las variables inyectables (tema, tono, texto fuente,
duración, hashtags, perfil de cliente).

El contenido se orienta al nicho político: serio, directo, sin lenguaje informal,
sin emojis en el tono confrontacional, con datos duros y estructura argumentativa.

## Criterios de Aceptación

- [ ] Módulo `tiktok_reels.py` genera guion técnico en 2 columnas (VOZ / VISUAL)
- [ ] Módulo `twitter_threads.py` genera hilo de 5 a 10 tweets con gancho inicial
- [ ] Módulo `social_posts.py` genera carrusel con estructura P.A.S.C. e IG copy largo
- [ ] Todos los prompts aceptan: texto fuente, tema, tono, duración, perfil de cliente
- [ ] Tono configurable: "confrontacional", "educativo", "motivacional", "urgente"
- [ ] Integración con el perfil `clients/lla_chascomus.json` (hashtags, estilo, temas)
- [ ] Resultado de cada prompt es un dict estructurado (no texto plano sin formato)

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `src/scripts/tiktok_reels.py`
- [NEW] `src/scripts/twitter_threads.py`
- [NEW] `src/scripts/social_posts.py`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido llamar directamente a APIs (usar `api_manager.py` de ISS-006)
- Prohibido hardcodear contenido específico de LLA (usar perfil del cliente)
- Prohibido usar emojis en los prompts del tono "confrontacional" y "serio"

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -c "
from src.scripts.tiktok_reels import get_prompt
prompt = get_prompt(
    texto='El deficit fiscal era del 5 porciento del PBI.',
    tono='confrontacional',
    duracion=60,
    cliente={'hashtags_fijos': ['#Milei', '#LLA']}
)
assert 'system' in prompt, 'Falta system prompt'
assert 'user' in prompt, 'Falta user prompt'
assert len(prompt['user']) > 100, 'Prompt demasiado corto'
print('OK: Prompt TikTok generado correctamente')
"
```

---

## Especificación de Prompts

### TikTok / Reels (60s, guion técnico)

**Formato de salida esperado:**
```json
{
  "titulo": "El déficit que nos dejaron",
  "duracion": 60,
  "slides": [
    {
      "seg": "00:00–00:08",
      "voz": "El gobierno anterior dejó un déficit del 5% del PBI.",
      "visual": "B-Roll: gráfico de barras descendente. Texto en pantalla: -5% PBI",
      "efecto": "Música tensa instrumental. Zoom lento hacia el gráfico."
    }
  ],
  "hashtags": ["#Milei", "#LLA", "#LibertadAvanza"],
  "cta": "Seguinos para más datos que no te cuentan."
}
```

### X / Twitter (hilo viral)

**Formato de salida esperado:**
```json
{
  "gancho": "El déficit que heredamos podría haber hundido a la Argentina. Hilo [1/8]",
  "tweets": [
    {"num": 1, "texto": "El gobierno anterior dejó un déficit del 5% del PBI. Para ponerlo en perspectiva..."},
    {"num": 2, "texto": "Eso equivale a imprimir $X por día solo para cubrir gastos corrientes..."},
    ...
    {"num": 8, "texto": "La libertad económica no se negocia. RT si entendés la diferencia. #Milei #LLA"}
  ]
}
```

### Instagram / Facebook (carrusel P.A.S.C.)

**Formato de salida esperado:**
```json
{
  "tipo": "carousel",
  "slides": [
    {"num": 1, "titulo": "¿Sabías que Argentina heredó el déficit más alto en décadas?", "tipo": "gancho"},
    {"num": 2, "titulo": "El déficit llegó al 5% del PBI", "cuerpo": "...", "tipo": "problema"},
    {"num": 3, "cuerpo": "Cada argentino pagó $X de deuda por este desastre.", "tipo": "agitacion"},
    {"num": 4, "titulo": "La solución: superávit primario en 12 meses.", "tipo": "solucion"},
    {"num": 5, "cta": "¿Estás de acuerdo? Comentá abajo.", "tipo": "cierre"}
  ],
  "copy_caption": "El déficit que heredamos era insostenible...\n\n#Milei #LLA #LibertadAvanza"
}
```
