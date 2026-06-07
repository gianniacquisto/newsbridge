from datetime import datetime, timedelta, timezone

import pytest_asyncio


@pytest_asyncio.fixture
async def articles_with_sources(client):
    """Insert articles and sources into the test database."""
    from backend import database

    async with database.get_db() as db:
        # Insert an article from De Standaard (Dutch)
        cursor = await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.standaard.be/article1",
                "Belgische verkiezingen: wat moet u weten",
                1,
                (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
                "Volledige artikeltekst in het Nederlands...",
                "nl",
            ),
        )
        await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.lesoir.be/article2",
                "Élections belges: ce qu'il faut savoir",
                6,
                (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat(),
                "Texte complet de l'article en français...",
                "fr",
            ),
        )
        await db.execute(
            """
            INSERT INTO articles (url, title, source_id, published_at, content, source_language)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "https://www.vrt.be/article3",
                "Weerbericht: regen vandaag",
                3,
                (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
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
    titles = [a["title"] for a in articles]

    # Verify our 3 articles are present
    assert "Élections belges: ce qu'il faut savoir" in titles
    assert "Belgische verkiezingen: wat moet u weten" in titles
    assert "Weerbericht: regen vandaag" in titles

    # Verify sort order: find indices
    fr_idx = titles.index("Élections belges: ce qu'il faut savoir")
    nl_idx = titles.index("Belgische verkiezingen: wat moet u weten")
    vrt_idx = titles.index("Weerbericht: regen vandaag")

    assert fr_idx < nl_idx < vrt_idx, "Articles should be sorted newest-first"
