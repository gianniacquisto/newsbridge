from datetime import datetime

from pydantic import BaseModel


class Source(BaseModel):
    id: int
    name: str
    url: str
    source_language: str | None = None
    created_at: datetime


class Article(BaseModel):
    id: int
    url: str
    title: str
    source_id: int
    source_name: str | None = None
    published_at: datetime | None = None
    content: str | None = None
    source_language: str | None = None
    created_at: datetime


class ArticleOut(Article):
    """Article with source name included."""
    source_name: str | None = None


class Translation(BaseModel):
    id: int
    article_id: int
    target_language: str
    translated_content: str | None = None
    status: str
    created_at: datetime
    completed_at: datetime | None = None


class ArticleWithTranslation(Article):
    """Article with its translation (if any)."""
    translation: Translation | None = None


class HealthCheck(BaseModel):
    status: str
