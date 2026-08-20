# Guion-Gen

Fábrica y suite interactiva local de generación de guiones y contenido multimedia para redes sociales (Instagram, Facebook, X, TikTok), con ingesta de audio/video, transcripción con timestamps a Markdown (.md), generación multicanal y manipulación con FFmpeg.

---

## Características

- **Ingesta y Transcripción:** Procesamiento de conferencias y audios largos (Groq Whisper / faster-whisper) con exportación a `.md`.
- **Fábrica de Guiones:** Creación de guiones adaptados a TikTok/Reels (2 columnas), hilos para X y carruseles P.A.S.C. para Instagram/Facebook.
- **Motor Visual Dual:** Plantillas CSS listas para exportar PNG con Playwright y generación de fondos con IA.
- **Herramientas de Medios:** Recorte de clips con FFmpeg y exportación de subtítulos sincronizados `.srt` / `.vtt`.

---

## Arranque Rápido (Iniciar Servidor)

Para levantar el servidor web local y acceder a la suite interactiva de Guion-Gen, ejecuta el siguiente comando en la raíz del proyecto:

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

*(Alternativamente: activar el entorno con `.\venv\Scripts\Activate.ps1` y ejecutar `streamlit run app.py`).*

La interfaz abrirá automáticamente en `http://localhost:8501`.

---

## Documentación Técnica

La especificación completa del proyecto se encuentra en la carpeta [`documentacion/`](./documentacion/):
- [Índice Maestro de Issues (`documentacion/INDEX.md`)](./documentacion/INDEX.md)
- [Perfil de Marca LLA Chascomus (`documentacion/ISS-018_perfil-marca-lla.md`)](./documentacion/ISS-018_perfil-marca-lla.md)
