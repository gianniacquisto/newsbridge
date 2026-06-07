from datetime import datetime, timezone

import pytest_asyncio


@pytest_asyncio.fixture
async def article_with_cached_translation(client):
    """Insert an article with an existing translated title."""
    from backend import database

    async with database.get_db() as db:
        cursor = await db.execute(
            """
            INSERT INTO articles (url, title, translated_title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.standaard.be/cached",
                "Gecacheld Artikel",
                "Cached Article",
                1,
                datetime.now(timezone.utc).isoformat(),
                "Inhoud die al vertaald is...",
                "nl",
            ),
        )
        article_id = cursor.lastrowid
        await db.commit()
        return article_id


def test_translate_returns_cached(client, article_with_cached_translation):
    """POST /articles/{id}/translate returns existing translation when already completed."""
    response = client.post(f"/api/articles/{article_with_cached_translation}/translate")
    assert response.status_code == 200

    data = response.json()
    assert data["translated_title"] == "Cached Article"
    assert data["article_id"] == article_with_cached_translation
