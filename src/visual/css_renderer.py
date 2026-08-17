"""Motor de renderizado CSS/HTML a PNG mediante Playwright Asincrónico y Concurrencia."""
import os
import time
import zipfile
import asyncio
import concurrent.futures
from pathlib import Path
from playwright.async_api import async_playwright

from src.visual.html_renderer import render_template_to_html
from src.config.settings import OUTPUT_DIR, BASE_DIR, MEDIA_FORMATS, load_client_profile

FORMATS = {
    "4:5": {"width": 1080, "height": 1350},
    "9:16": {"width": 1080, "height": 1920},
    "1:1": {"width": 1080, "height": 1080},
    "16:9": {"width": 1920, "height": 1080}
}

def _run_async(coro):
    """Ejecuta una corrutina de forma segura incluso si ya existe un event loop activo."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)

async def _render_single_page(page, html_content: str, output_path: Path) -> dict:
    """Renderiza el contenido HTML en una página de Playwright y captura el screenshot."""
    t0 = time.time()
    await page.set_content(html_content, wait_until="networkidle")

    # Inspección DOM anti-overflow y auto-escala
    await page.evaluate("""
    () => {
        const wrapper = document.querySelector('.slide-wrapper') || document.body;
        const main = document.querySelector('.slide-main');
        if (wrapper.scrollHeight > wrapper.clientHeight || (main && main.scrollHeight > main.clientHeight)) {
            wrapper.style.transform = 'scale(0.9)';
            wrapper.style.transformOrigin = 'top center';
        }
    }
    """)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    await page.screenshot(path=str(output_path), type="png")
    
    elapsed = time.time() - t0
    size = output_path.stat().st_size if output_path.exists() else 0

    return {
        "path": str(output_path),
        "size_bytes": size,
        "elapsed_sec": round(elapsed, 3)
    }

async def async_render_slide(
    template: str,
    data: dict,
    output_path: str,
    formato: str = "4:5",
    client: dict = None
) -> dict:
    """
    Renderiza un slide individual de forma asincrónica.
    """
    t_start = time.time()
    html_content = render_template_to_html(template, data, client=client)
    out_p = Path(output_path)
    if not out_p.is_absolute():
        out_p = BASE_DIR / output_path

    viewport = FORMATS.get(formato, FORMATS["4:5"])

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=viewport,
            device_scale_factor=2
        )
        page = await context.new_page()
        try:
            res = await _render_single_page(page, html_content, out_p)
            res["total_elapsed_sec"] = round(time.time() - t_start, 3)
            return res
        finally:
            await context.close()
            await browser.close()

async def async_render_carousel(
    template: str,
    slides_data: list[dict],
    proyecto: str,
    formato: str = "4:5",
    client: dict = None
) -> dict:
    """
    Renderiza todos los slides de un carrusel en paralelo utilizando asyncio.gather.
    """
    t_start = time.time()
    total = len(slides_data)
    out_dir = OUTPUT_DIR / proyecto / "carrusel"
    out_dir.mkdir(parents=True, exist_ok=True)

    viewport = FORMATS.get(formato, FORMATS["4:5"])

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=viewport,
            device_scale_factor=2
        )

        async def _worker(idx: int, slide_dict: dict):
            page = await context.new_page()
            try:
                # Inyectar numeración contractual
                s_data = dict(slide_dict)
                s_data["slide_num"] = idx + 1
                s_data["total_slides"] = total
                
                html_str = render_template_to_html(template, s_data, client=client)
                slide_path = out_dir / f"slide_{idx+1:02d}.png"
                return await _render_single_page(page, html_str, slide_path)
            finally:
                await page.close()

        tasks = [_worker(i, s) for i, s in enumerate(slides_data)]
        results = await asyncio.gather(*tasks)

        await context.close()
        await browser.close()

    # Generar archivo ZIP con todos los slides
    zip_path = OUTPUT_DIR / proyecto / f"carrusel_{proyecto}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for r in results:
            png_p = Path(r["path"])
            if png_p.exists():
                zipf.write(png_p, arcname=png_p.name)

    total_elapsed = round(time.time() - t_start, 3)

    return {
        "slides": [r["path"] for r in results],
        "slides_detail": results,
        "zip": str(zip_path),
        "total_elapsed_sec": total_elapsed,
        "formato": formato,
        "total_slides": total
    }

def render_slide(
    template: str,
    data: dict,
    output_path: str,
    formato: str = "4:5",
    client: dict = None
) -> dict:
    """Wrapper sincrónico para renderizar un slide individual."""
    return _run_async(
        async_render_slide(
            template=template,
            data=data,
            output_path=output_path,
            formato=formato,
            client=client
        )
    )

def render_carousel(
    template: str,
    slides_data: list[dict],
    proyecto: str,
    formato: str = "4:5",
    client: dict = None
) -> dict:
    """Wrapper sincrónico para renderizar un carrusel concurrente."""
    return _run_async(
        async_render_carousel(
            template=template,
            slides_data=slides_data,
            proyecto=proyecto,
            formato=formato,
            client=client
        )
    )
