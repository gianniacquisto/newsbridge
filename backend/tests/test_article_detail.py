from datetime import datetime, timezone

import pytest_asyncio


@pytest_asyncio.fixture
async def article_with_translation(client):
    """Insert an article with a cached translation."""
    from backend import database

    db_path = database.settings.database_url.replace("sqlite+aiosqlite:///", "")
    async with database.get_db() as db:
        # Insert article (auto-increment ID)
        cursor = await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.standaard.be/special-article",
                "Speciaal Artikel: Belgische Politiek",
                1,
                datetime.now(timezone.utc).isoformat(),
                "Dit is de volledige inhoud van het artikel...",
                "nl",
            ),
        )
        article_id = cursor.lastrowid

        # Insert translation
        await db.execute(
            """
            INSERT INTO translations (article_id, target_language, translated_content, status, completed_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (article_id, "en", "Special Article: Belgian Politics\n\nThis is the full content...", "completed", datetime.now(timezone.utc).isoformat()),
        )

        await db.commit()
        return article_id


def test_get_article_with_translation(client, article_with_translation):
    """GET /articles/{id} returns the article with its cached translation."""
    response = client.get(f"/articles/{article_with_translation}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Speciaal Artikel: Belgische Politiek"
    assert data["source_language"] == "nl"
    assert data["content"] == "Dit is de volledige inhoud van het artikel..."

    assert data["translation"] is not None
    assert data["translation"]["target_language"] == "en"
    assert "Belgian Politics" in data["translation"]["translated_content"]
    assert data["translation"]["status"] == "completed"
