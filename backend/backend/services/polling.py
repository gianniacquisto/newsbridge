"""RSS polling service: fetch feeds on a schedule and store articles."""

import asyncio
import logging

from typing import Any
import feedparser

from backend.database import get_db
from backend.config import settings

logger = logging.getLogger(__name__)

# Target language for title translation (global setting)
TARGET_LANGUAGE = "en"


def _parse_published(parsed):
    """Convert a time.struct_time to ISO format string, or return None."""
    if parsed is None:
        return None
    try:
        import datetime
        return datetime.datetime(*parsed[:6]).isoformat()
    except (ValueError, TypeError):
        return None


async def _fetch_feed(source: dict) -> list[dict]:
    """Fetch a single RSS feed and return list of articles."""
    feed = feedparser.parse(source["url"])
    articles = []

    for entry in feed.entries:
        articles.append({
            "url": entry.get("link", ""),
            "title": entry.get("title", ""),
            "published": _parse_published(entry.get("published_parsed")),
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
                INSERT OR IGNORE INTO articles (url, title, translated_title, source_id, published_at, content, source_language)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    art["url"],
                    art["title"],
                    None,  # translated_title will be filled in by title translation
                    source_id,
                    art["published"],
                    art["content"],
                    source_lang,
                ),
            )
        await db.commit()


async def _translate_titles():
    """Translate titles for articles that don't have a translated title yet."""
    from backend.services.translation import translate_title

    async with get_db() as db:
        # Find articles without translated titles
        cursor = await db.execute(
            "SELECT id, title, source_language FROM articles WHERE translated_title IS NULL"
        )
        articles = await cursor.fetchall()

        # Batch translate titles (limit to avoid overwhelming the LLM)
        batch_size = 5
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            tasks = []
            for art in batch:
                tasks.append(translate_title(
                    art["title"],
                    art["source_language"],
                    TARGET_LANGUAGE,
                ))

            translated = await asyncio.gather(*tasks, return_exceptions=True)

            # Update articles with translated titles
            async with get_db() as db:
                for art, trans_title in zip(batch, translated):
                    if isinstance(trans_title, Exception):
                        logger.exception("Title translation failed for article %d", art["id"])
                        continue
                    if trans_title:
                        await db.execute(
                            "UPDATE articles SET translated_title = ? WHERE id = ?",
                            (trans_title, art["id"]),
                        )
                        await db.commit()
                        logger.info("Translated title: '%s' -> '%s'", art["title"], trans_title)


async def poll_all():
    """Fetch all RSS feeds and store new articles, then translate titles."""
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM sources")
        sources = await cursor.fetchall()

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

    # Translate titles for newly fetched articles
    await _translate_titles()


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
