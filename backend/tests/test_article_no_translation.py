from datetime import datetime, timezone

import pytest_asyncio


@pytest_asyncio.fixture
async def article_without_translation(client):
    """Insert an article with no translation."""
    from backend import database

    async with database.get_db() as db:
        cursor = await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.knack.be/no-trans-yet",
                "Geen Vertaling",
                4,
                datetime.now(timezone.utc).isoformat(),
                "Inhoud zonder vertaling...",
                "nl",
            ),
        )
        article_id = cursor.lastrowid
        await db.commit()
        return article_id


def test_get_article_without_translation(client, article_without_translation):
    """GET /articles/{id} returns null translation when none exists."""
    response = client.get(f"/api/articles/{article_without_translation}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Geen Vertaling"
    assert data["translation"] is None


def test_get_nonexistent_article(client):
    """GET /articles/{id} returns 404 for unknown article."""
    response = client.get("/api/articles/99999")
    assert response.status_code == 404
