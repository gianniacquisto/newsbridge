from datetime import datetime, timedelta, timezone

import pytest_asyncio


@pytest_asyncio.fixture
async def articles_with_sources(db_dir):
    """Insert articles and sources into the test database."""
    from backend import database

    # The init_db fixture has already seeded sources, so we can insert articles
    db_path = database.settings.database_url.replace("sqlite+aiosqlite:///", "")
    async with database.get_db() as db:
        # Insert an article from De Standaard (Dutch)
        await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.standaard.be/article1",
                "Belgische verkiezingen: wat moet u weten",
                1,
                datetime.now(timezone.utc) - timedelta(hours=2),
                "Volledige artikeltekst in het Nederlands...",
                "nl",
            ),
        )

        # Insert an article from Le Soir (French), more recent
        await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.lesoir.be/article2",
                "Élections belges: ce qu'il faut savoir",
                6,
                datetime.now(timezone.utc) - timedelta(minutes=30),
                "Texte complet de l'article en français...",
                "fr",
            ),
        )

        # Insert an older article from VRT NWS
        await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.vrt.be/article3",
                "Weerbericht: regen vandaag",
                3,
                datetime.now(timezone.utc) - timedelta(days=1),
                "Weerbericht inhoud...",
                "nl",
            ),
        )

        await db.commit()


def test_get_articles_returns_sorted_by_newest(client, articles_with_sources):
    """GET /articles returns articles sorted by most recent first."""
    response = client.get("/articles")
    assert response.status_code == 200

    articles = response.json()
    assert len(articles) == 3

    # Most recent should be first (30 min ago)
    assert articles[0]["title"] == "Élections belges: ce qu'il faut savoir"

    # Oldest should be last (1 day ago)
    assert articles[2]["title"] == "Weerbericht: regen vandaag"
