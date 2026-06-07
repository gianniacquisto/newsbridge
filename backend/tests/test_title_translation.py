"""Tests for title translation during polling."""

from datetime import datetime, timezone

import pytest_asyncio


@pytest_asyncio.fixture
async def article_with_translated_title(client):
    """Insert an article with a translated title."""
    from backend import database

    async with database.get_db() as db:
        await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language, translated_title)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.standaard.be/translated-title",
                "Speciaal Artikel",
                1,
                datetime.now(timezone.utc).isoformat(),
                "Inhoud...",
                "nl",
                "Special Article",
            ),
        )
        await db.commit()


def test_get_articles_returns_translated_title(client, article_with_translated_title):
    """GET /articles returns translated_title when available."""
    response = client.get("/api/articles")
    assert response.status_code == 200

    articles = response.json()
    article = [a for a in articles if a["url"] == "https://www.standaard.be/translated-title"][0]
    assert article["translated_title"] == "Special Article"


def test_get_articles_fallback_to_original_when_no_translation(client):
    """GET /articles returns original title when translated_title is null."""
    from datetime import datetime, timezone

    from backend import database

    async def _insert():
        async with database.get_db() as db:
            await db.execute(
                """
                INSERT INTO articles (url, title, source_id, published_at, content, source_language, translated_title)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "https://www.vrt.be/no-trans-title",
                    "Originele Titel",
                    3,
                    datetime.now(timezone.utc).isoformat(),
                    "Inhoud...",
                    "nl",
                    None,
                ),
            )
            await db.commit()

    import asyncio
    asyncio.get_event_loop().run_until_complete(_insert())

    response = client.get("/api/articles")
    assert response.status_code == 200

    articles = response.json()
    article = [a for a in articles if a["url"] == "https://www.vrt.be/no-trans-title"][0]
    assert article["translated_title"] == "Originele Titel"
