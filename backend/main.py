from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.services.polling import start_polling, stop_polling

# --- App startup/shutdown ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    scheduler = AsyncIOScheduler()
    app.state.scheduler = scheduler
    start_polling(scheduler)
    scheduler.start()
    yield
    stop_polling(scheduler)
    scheduler.shutdown()


app = FastAPI(
    title="Newsbridge",
    description="Belgian news, translated to your language.",
    version="0.1.0",
    lifespan=lifespan,
)

api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Placeholder routes ---


@api_router.get("/")
async def root():
    return {"message": "Newsbridge API"}


@api_router.get("/health")
async def health():
    return {"status": "ok"}


# --- API routes ---


@api_router.get("/sources")
async def get_sources():
    from backend.database import get_db

    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM sources")
        sources = await cursor.fetchall()
        return [dict(s) for s in sources]


@api_router.get("/articles")
async def get_articles():
    from backend.database import get_db

    async with get_db() as db:
        cursor = await db.execute(
            """
            SELECT a.*, s.name as source_name
            FROM articles a
            JOIN sources s ON a.source_id = s.id
            ORDER BY a.published_at DESC
            """
        )
        articles = await cursor.fetchall()
        result = []
        for a in articles:
            article = dict(a)
            # Fallback to original title if translated_title is null
            if article["translated_title"] is None:
                article["translated_title"] = article["title"]
            result.append(article)
        return result


@api_router.get("/articles/{article_id}")
async def get_article(article_id: int):
    from backend.database import get_db

    async with get_db() as db:
        # Fetch article with source name
        cursor = await db.execute(
            """
            SELECT a.*, s.name as source_name
            FROM articles a
            JOIN sources s ON a.source_id = s.id
            WHERE a.id = ?
            """,
            (article_id,),
        )
        article_row = await cursor.fetchone()
        if not article_row:
            raise HTTPException(status_code=404, detail="Article not found")

        article = dict(article_row)

        # Fetch cached translation
        cursor = await db.execute(
            "SELECT * FROM translations WHERE article_id = ?",
            (article_id,),
        )
        translation_row = await cursor.fetchone()
        article["translation"] = dict(translation_row) if translation_row else None

        return article


@api_router.post("/articles/{article_id}/translate")
async def translate_article(article_id: int):
    from backend.database import get_db

    async with get_db() as db:
        # Check if already translated
        cursor = await db.execute(
            "SELECT id, title, translated_title FROM articles WHERE id = ?",
            (article_id,),
        )
        art_row = await cursor.fetchone()
        if not art_row:
            raise HTTPException(status_code=404, detail="Article not found")

        # If already translated, return existing
        if art_row["translated_title"] is not None:
            return {"article_id": article_id, "translated_title": art_row["translated_title"]}

    # Trigger background translation
    from backend.services.polling import _translate_article, _launch_background
    _launch_background(_translate_article, article_id)
    return {"status": "queued", "article_id": article_id}

app.include_router(api_router)
