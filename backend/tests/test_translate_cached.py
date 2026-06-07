from datetime import datetime, timezone

import pytest_asyncio


@pytest_asyncio.fixture
async def article_with_cached_translation(client):
    """Insert an article with a completed translation."""
    from backend import database

    async with database.get_db() as db:
        cursor = await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.standaard.be/cached",
                "Gecacheld Artikel",
                1,
                datetime.now(timezone.utc).isoformat(),
                "Inhoud die al vertaald is...",
                "nl",
            ),
        )
        article_id = cursor.lastrowid

        await db.execute(
            """
            INSERT INTO translations (article_id, target_language, translated_content, status, completed_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (article_id, "en", "Cached Article\n\nContent already translated...", "completed", datetime.now(timezone.utc).isoformat()),
        )

        await db.commit()
        return article_id


def test_translate_returns_cached(client, article_with_cached_translation):
    """POST /articles/{id}/translate returns existing translation when already completed."""
    response = client.post(f"/articles/{article_with_cached_translation}/translate")
    assert response.status_code == 200

    data = response.json()
    assert data["translated_content"] == "Cached Article\n\nContent already translated..."
    assert data["status"] == "completed"
    assert data["target_language"] == "en"
