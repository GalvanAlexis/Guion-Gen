"""Tests unitarios y de integración para los generadores de prompts por red social."""
import pytest
from src.scripts.tiktok_reels import get_tiktok_prompt
from src.scripts.twitter_threads import get_twitter_prompt
from src.scripts.social_posts import get_social_post_prompt
from src.config.api_manager import APIManager

SAMPLE_TEXT = (
    "El déficit fiscal que heredamos era del cinco por ciento del PBI. "
    "Durante décadas se financió el descalabro con emisión monetaria e inflación descontrolada. "
    "En solo doce meses logramos superávit financiero y primario por primera vez en la historia moderna."
)

def test_tiktok_prompt_structure():
    """Verifica la construcción del prompt de TikTok."""
    prompt = get_tiktok_prompt(
        texto_fuente=SAMPLE_TEXT,
        tono="confrontacional",
        tema="Déficit fiscal heredado",
        duracion=60
    )
    assert "system" in prompt
    assert "user" in prompt
    assert "60" in prompt["user"]
    assert "Déficit fiscal" in prompt["user"]
    assert prompt["red"] == "tiktok"

def test_twitter_prompt_structure():
    """Verifica la construcción del prompt de X (Twitter)."""
    prompt = get_twitter_prompt(
        texto_fuente=SAMPLE_TEXT,
        tono="confrontacional",
        tema="Superávit histórico",
        cantidad_tweets=5
    )
    assert "system" in prompt
    assert "user" in prompt
    assert "5" in prompt["user"]
    assert prompt["red"] == "twitter"

def test_social_posts_prompt_structure():
    """Verifica la construcción del prompt de Instagram y Facebook."""
    ig_prompt = get_social_post_prompt(
        texto_fuente=SAMPLE_TEXT,
        red="instagram",
        tono="educativo",
        tema="Reforma económica",
        cantidad_slides=5
    )
    assert ig_prompt["red"] == "instagram"
    assert "P.A.S.C." in ig_prompt["system"]
    assert "5" in ig_prompt["user"]

    fb_prompt = get_social_post_prompt(
        texto_fuente=SAMPLE_TEXT,
        red="facebook",
        tono="educativo",
        tema="Reforma económica"
    )
    assert fb_prompt["red"] == "facebook"

def test_prompt_generation_with_llm():
    """Verifica que el LLM procese un prompt de TikTok y devuelva JSON válido con slides."""
    mgr = APIManager()
    prompt_pkg = get_tiktok_prompt(
        texto_fuente=SAMPLE_TEXT,
        tono="confrontacional",
        tema="Déficit vs Superávit",
        duracion=30
    )
    
    res = mgr.generate_json(
        prompt=prompt_pkg["user"],
        system_prompt=prompt_pkg["system"],
        temperature=0.3
    )

    assert "data" in res
    data = res["data"]
    assert "titulo" in data
    assert "slides" in data
    assert len(data["slides"]) >= 1
    assert "voz" in data["slides"][0]
    assert "visual" in data["slides"][0]
