import aiosqlite
from contextlib import asynccontextmanager

from backend.config import settings

# Schema migrations applied at startup
SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    source_language TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    published_at TIMESTAMP,
    content TEXT,
    source_language TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    target_language TEXT NOT NULL,
    translated_content TEXT,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending, completed, failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(id)
);

CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source_id);
CREATE INDEX IF NOT EXISTS idx_translations_article ON translations(article_id);
CREATE INDEX IF NOT EXISTS idx_translations_status ON translations(status);
"""


@asynccontextmanager
async def get_db():
    db = await aiosqlite.connect(settings.database_url.replace("sqlite+aiosqlite:///", ""))
    db.row_factory = aiosqlite.Row
    yield db
    await db.close()


async def init_db():
    """Create tables and insert default sources."""
    db_path = settings.database_url.replace("sqlite+aiosqlite:///", "")
    async with aiosqlite.connect(db_path) as db:
        await db.executescript(SCHEMA)

        # Insert default Belgian sources
        defaults = [
            ("De Standaard", "https://www.standaard.be/rss/", "nl"),
            ("De Morgen", "https://www.demorgen.be/rss/", "nl"),
            ("VRT NWS", "https://www.vrt.be/vrtnws/nl.rss", "nl"),
            ("Knack", "https://www.knack.be/news/index.rdf", "nl"),
            ("De Tijd", "https://www.tijd.be/rss/", "nl"),
            ("Le Soir", "https://www.lesoir.be/rss/all", "fr"),
            ("La Libre Belgique", "https://www.lalibre.be/rss/", "fr"),
            ("RTBF Info", "https://www.rtbf.be/info/radio/rss/mr/rtvbrtinforss", "fr"),
            ("L'Echo", "https://www.lecho.be/rss/", "fr"),
        ]

        await db.executemany(
            """
            INSERT OR IGNORE INTO sources (name, url, source_language)
            VALUES (?, ?, ?)
            """,
            defaults,
        )

        await db.commit()
