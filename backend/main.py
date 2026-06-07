from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services.polling import start_polling, stop_polling

# --- App startup/shutdown ---


@asynccontextmanager
async def lifespan(app: FastAPI):
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Placeholder routes ---


@app.get("/")
async def root():
    return {"message": "Newsbridge API"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# --- API routes ---


@app.get("/sources")
async def get_sources():
    from backend.database import get_db

    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM sources")
        sources = await cursor.fetchall()
        return [dict(s) for s in sources]


@app.get("/articles")
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
        return [dict(a) for a in articles]
