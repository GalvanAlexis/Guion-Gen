# ISS-001 — Setup del Entorno Base

**Tipo:** `chore`
**Sesión:** 1
**Prioridad:** Alta
**Dependencias:** Ninguna
**Branch:** `feature/ISS-001_setup-entorno-base`

---

## Descripción

Crear la estructura completa del proyecto, verificar e instalar FFmpeg en el sistema,
inicializar el entorno virtual de Python, instalar dependencias base y levantar
el esqueleto de la aplicación Streamlit con la paleta oscura LLA y navegación lateral.

## Criterios de Aceptación

- [x] `ffmpeg` disponible en PATH del sistema (verificación con `ffmpeg -version`)
- [x] Entorno virtual Python 3.11+ creado en `.venv/`
- [x] `requirements.txt` con todas las dependencias fijadas con versión
- [x] Estructura de carpetas completa según arquitectura del plan maestro
- [x] `app.py` corre sin errores con `streamlit run app.py`
- [x] Sidebar visible con las 5 pestañas navegables (sin contenido real aún)
- [x] Paleta de colores LLA aplicada (fondo `#0a0a10`, acento `#8B5CF6`)
- [x] Barra de estado inferior visible con indicadores de APIs
- [x] `.env.example` creado con todas las variables necesarias
- [x] `.gitignore` configurado (excluye `.env`, `.venv/`, `output/`, `temp/`)

## Archivos a Crear / Modificar

### 🎯 Target Files Permitidos

- [NEW] `requirements.txt`
- [NEW] `.env.example`
- [NEW] `.gitignore`
- [NEW] `app.py`
- [NEW] `src/__init__.py`
- [NEW] `src/config/__init__.py`
- [NEW] `src/config/settings.py`
- [NEW] `src/core/__init__.py`
- [NEW] `src/scripts/__init__.py`
- [NEW] `src/visual/__init__.py`
- [NEW] `src/ui/__init__.py`
- [NEW] `src/ui/components.py`
- [NEW] `src/ui/tab_fuente.py` (placeholder)
- [NEW] `src/ui/tab_guion.py` (placeholder)
- [NEW] `src/ui/tab_visual.py` (placeholder)
- [NEW] `src/ui/tab_media.py` (placeholder)
- [NEW] `src/ui/tab_biblioteca.py` (placeholder)
- [NEW] `clients/lla_chascomus.json` (esqueleto)
- [NEW] `output/.gitkeep`
- [NEW] `temp/.gitkeep`

### 🚫 Acciones Prohibidas (Guardrails)

- Prohibido instalar paquetes no listados en requirements.txt sin aprobación
- Prohibido crear archivos fuera de la estructura definida
- Prohibido escribir lógica de negocio real en los placeholders de tabs
- Prohibido modificar archivos del sistema o del entorno global de Python

### 🧪 Quality Gate Determinista

```powershell
cd "c:\Users\PC Blado\Desktop\BladoPC\Dev\Guion-Gen"
.venv\Scripts\python -m streamlit run app.py --server.headless true &
Start-Sleep 5; Invoke-WebRequest http://localhost:8501 -UseBasicParsing | Select-Object StatusCode
```

Resultado esperado: `StatusCode: 200`

---

## Notas Técnicas

**FFmpeg en Windows (winget):**
```powershell
winget install --id Gyan.FFmpeg -e --source winget
```

**Entorno virtual:**
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Contenido mínimo de `requirements.txt`:**
```
streamlit>=1.39.0
faster-whisper>=1.0.3
yt-dlp>=2024.10.1
groq>=0.11.0
google-genai>=0.7.0
python-dotenv>=1.0.1
pillow>=10.4.0
playwright>=1.47.0
jinja2>=3.1.4
ffmpeg-python>=0.2.0
```
