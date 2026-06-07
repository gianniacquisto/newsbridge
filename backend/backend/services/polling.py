"""RSS polling service: fetch feeds on a schedule and store articles."""

import asyncio
import logging

from typing import Any
import feedparser

from backend.database import get_db
from backend.config import settings

logger = logging.getLogger(__name__)

# Track background translation tasks so they are not garbage-collected
_active_translation_tasks: set[asyncio.Task] = set()


def _on_translation_done(task: asyncio.Task) -> None:
    """Log errors from finished background translation tasks and untrack them."""
    if error := task.exception():
        logger.exception("Background translation task failed")
    _active_translation_tasks.discard(task)


def _launch_background(fn, *args, **kwargs):
    """Launch a coroutine as a background task with tracking."""
    task = asyncio.create_task(fn(*args, **kwargs))
    _active_translation_tasks.add(task)
    task.add_done_callback(_on_translation_done)

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


async def _translate_article(article_id: int) -> None:
    """Translate a single article's title and full content."""
    from backend.services.translation import translate_article, translate_title

    async with get_db() as db:
        cursor = await db.execute(
            "SELECT id, title, source_language, content FROM articles WHERE id = ?",
            (article_id,),
        )
        art_row = await cursor.fetchone()
        if not art_row:
            logger.info("Article %d does not exist", article_id)
            return

        title = art_row["title"]
        source_lang = art_row["source_language"]
        content = art_row["content"]

        # --- Translate title ---
        cursor = await db.execute(
            "SELECT id FROM articles WHERE id = ? AND translated_title IS NULL",
            (article_id,),
        )
        if not await cursor.fetchone():
            logger.info("Article %d already has a translated title", article_id)
            return

        logger.info("Translating title: '%s'", title)
        translated_title = await translate_title(title, source_lang, TARGET_LANGUAGE)

        # --- Translate content ---
        logger.info("Translating content for article %d", article_id)
        translated_content = None
        if content:
            translated_content = await translate_article(
                title, content, source_lang, TARGET_LANGUAGE,
            )

        if not translated_title and not translated_content:
            logger.error("Both title and content translation returned None for article %d", article_id)
            return

        # Double-check: another background task may have beaten us here
        async with get_db() as db2:
            cursor = await db2.execute(
                "SELECT id, translated_title FROM articles WHERE id = ?",
                (article_id,),
            )
            existing = await cursor.fetchone()
            if not existing:
                logger.info("Article %d was deleted", article_id)
                return

            # Save translated content to translations table (upsert)
            if translated_content:
                await db2.execute(
                    "UPDATE translations SET translated_content = ?, status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE article_id = ?",
                    (translated_content, article_id),
                )
                if db2.total_changes == 0:
                    await db2.execute(
                        "INSERT INTO translations (article_id, target_language, translated_content, status, completed_at) VALUES (?, ?, ?, 'completed', CURRENT_TIMESTAMP)",
                        (article_id, TARGET_LANGUAGE, translated_content),
                    )

            # Save translated title if we got one
            if translated_title and existing["translated_title"] is None:
                await db2.execute(
                    "UPDATE articles SET translated_title = ? WHERE id = ?",
                    (translated_title, article_id),
                )

            await db2.commit()
            logger.info("Translated article %d: title='%s' content_len=%d",
                        article_id, translated_title, len(translated_content or ""))


async def _translate_titles() -> list[asyncio.Task]:
    """Translate titles for articles that don't have a translated title yet.

    Returns the list of created tasks so callers can await them (e.g. in tests).
    In production this is wrapped by _launch_background for fire-and-forget behaviour.
    """
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT id, title, source_language FROM articles WHERE translated_title IS NULL"
        )
        articles = await cursor.fetchall()

    tasks: list[asyncio.Task] = []
    for art in articles:
        task = asyncio.create_task(_translate_article(art["id"]))
        task.add_done_callback(_on_translation_done)
        tasks.append(task)

    logger.info("Launched %d title translation(s) in background", len(tasks))
    return tasks


async def poll_all():
    """Fetch all RSS feeds and store new articles."""
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

    # Launch title translation as a background task (non-blocking)
    _launch_background(_translate_titles)


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
