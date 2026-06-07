"""RSS polling service: fetch feeds on a schedule and store articles."""

import logging

from typing import Any
import feedparser

from backend.database import get_db
from backend.config import settings

logger = logging.getLogger(__name__)


async def _fetch_feed(source: dict) -> list[dict]:
    """Fetch a single RSS feed and return list of articles."""
    feed = feedparser.parse(source["url"])
    articles = []

    for entry in feed.entries:
        articles.append({
            "url": entry.get("link", ""),
            "title": entry.get("title", ""),
            "published": entry.get("published_parsed"),
            "content": entry.get("summary", "") or entry.get("content", [{}])[0].get("value", ""),
            "source_language": source.get("source_language"),
        })

    return articles


async def _store_articles(source_id: int, source_lang: str, articles: list[dict]):
    """Store articles in the database, skipping duplicates."""
    async with get_db() as db:
        for art in articles:
            await db.execute(
                """
                INSERT OR IGNORE INTO articles (url, title, source_id, published_at, content, source_language)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    art["url"],
                    art["title"],
                    source_id,
                    art["published"],
                    art["content"],
                    source_lang,
                ),
            )
        await db.commit()


async def poll_all():
    """Fetch all RSS feeds and store new articles."""
    async with get_db() as db:
        sources = await db.execute("SELECT * FROM sources").fetchall()

        for source in sources:
            try:
                articles = await _fetch_feed(dict(source))
                if articles:
                    await _store_articles(source["id"], source["source_language"], articles)
                    logger.info(
                        "Fetched %d articles from %s",
                        len(articles),
                        source["name"],
                    )
            except Exception:
                logger.exception("Failed to fetch %s", source["name"])


def start_polling(scheduler: Any):
    """Start the RSS polling scheduler."""
    scheduler.add_job(
        poll_all,
        "interval",
        minutes=settings.poll_interval,
        id="rss_polling",
        replace_existing=True,
    )
    logger.info("Polling started (every %d min)", settings.poll_interval)


def stop_polling(scheduler: Any):
    """Stop the scheduler."""
    try:
        scheduler.shutdown(wait=False)
    except Exception:
        pass
