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

# --- Placeholder routes (will be fleshed out) ---


@app.get("/")
async def root():
    return {"message": "Newsbridge API"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# --- API routes (to be implemented) ---
# @app.get("/articles")
# @app.get("/articles/{article_id}")
# @app.post("/articles/{article_id}/translate")
# @app.get("/sources")
