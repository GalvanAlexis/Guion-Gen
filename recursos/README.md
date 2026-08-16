# Biblioteca de Recursos de Guion-Gen

Este directorio centraliza todos los activos estáticos, archivos multimedia originales y plantillas reutilizables para la producción de contenidos de la agencia y de LLA Chascomús.

---

## Estructura de Carpetas

```
recursos/
├── multimedia/     Archivos originales de video y audio (conferencias, discursos, entrevistas)
│   └── .gitkeep
├── plantillas/     Plantillas gráficas base, fondos pre-diseñados, logos y elementos vectoriales
│   └── .gitkeep
└── README.md       Instrucciones y lineamientos de organización
```

---

## Lineamientos de Almacenamiento

1. **Multimedia Original (`recursos/multimedia/`):**
   - Guardar aquí las grabaciones crudas, audios descargados y videos fuente antes de ser procesados por el pipeline.
   - Nomenclatura sugerida: `ORIGINAL_AAAA-MM-DD_descripcion-corta.ext` (ej: `ORIGINAL_2026-08-16_conferencia-milei.mp4`).

2. **Plantillas y Assets (`recursos/plantillas/`):**
   - Guardar aquí logotipos oficiales en PNG transparente de alta resolución, tipografías locales, marcas de agua, y esquemas de diseño base.
   - Los assets de marca como `lla_logo.png` deben ubicarse en esta carpeta para ser referenciados dinámicamente por el motor de renderizado visual.
