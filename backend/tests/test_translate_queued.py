from datetime import datetime, timezone

import pytest_asyncio


@pytest_asyncio.fixture
async def article_needing_translation(client):
    """Insert an article with no translation."""
    from backend import database

    async with database.get_db() as db:
        cursor = await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.vrt.be/new-article",
                "Nieuw Artikel",
                3,
                datetime.now(timezone.utc).isoformat(),
                "Nog niet vertaald...",
                "nl",
            ),
        )
        article_id = cursor.lastrowid
        await db.commit()
        return article_id


def test_translate_triggers_new_translation(client, article_needing_translation):
    """POST /articles/{id}/translate returns queued when no translation exists."""
    response = client.post(f"/articles/{article_needing_translation}/translate")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "queued"
