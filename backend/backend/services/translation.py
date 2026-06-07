"""Translation service: send articles to llama.cpp server for translation."""

import json
import logging

import httpx

from backend.config import settings

logger = logging.getLogger(__name__)

TRANSLATION_PROMPT = """\
You are a professional news translator. Translate the following article from {source_lang} to {target_lang}.

Rules:
- Preserve all facts, names, numbers, and quotes exactly
- Maintain the original tone and journalistic style
- Keep paragraph structure identical to the original
- Do not summarize, add commentary, or omit any content
- Output ONLY the translated text, no explanations

Article title: {title}

Article content:
{content}
"""

TITLE_TRANSLATION_PROMPT = """\
Translate this news article title from {source_lang} to {target_lang}:

{title}

Output ONLY the translated title, nothing else."""


async def translate_article(
    title: str,
    content: str,
    source_language: str,
    target_language: str,
) -> str | None:
    """Translate an article via the llama.cpp server."""
    prompt = TRANSLATION_PROMPT.format(
        source_lang=source_language,
        target_lang=target_language,
        title=title,
        content=content,
    )

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.llama_server_url}/v1/completions",
                json={
                    "model": settings.llm_model,
                    "prompt": prompt,
                    "max_tokens": settings.llm_max_tokens,
                    "temperature": settings.llm_temperature,
                    "stop": [],
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["text"].strip()
    except Exception:
        logger.exception("Translation failed for: %s", title)
        return None


async def translate_title(
    title: str,
    source_language: str,
    target_language: str,
) -> str | None:
    """Translate a short article title via the llama.cpp server."""
    prompt = TITLE_TRANSLATION_PROMPT.format(
        source_lang=source_language,
        target_lang=target_language,
        title=title,
    )

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.llama_server_url}/v1/completions",
                json={
                    "model": settings.llm_model,
                    "prompt": prompt,
                    "max_tokens": 200,
                    "temperature": settings.llm_temperature,
                    "stop": [],
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["text"].strip()
    except Exception:
        logger.exception("Title translation failed for: %s", title)
        return None
