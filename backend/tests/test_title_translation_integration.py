"""Integration test for title translation during polling."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest_asyncio


@pytest_asyncio.fixture
async def mock_llama_server():
    """Mock the llama.cpp server for title translation."""
    # Create a mock response object (not async)
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "choices": [{"text": "Translated Title"}]
    }
    
    # Create a mock async client
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.post = AsyncMock(return_value=mock_response)
    
    with patch("backend.services.translation.httpx.AsyncClient", return_value=mock_client):
        yield mock_client


def test_polling_translates_titles(mock_llama_server, client):
    """After polling, articles should have translated titles."""
    from backend import database

    async def _setup():
        async with database.get_db() as db:
            # Insert an article without translated title
            await db.execute(
                """
                INSERT INTO articles (url, title, source_id, published_at, content, source_language, translated_title)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "https://www.standaard.be/integration-test",
                    "Test Artikel",
                    1,
                    datetime.now(timezone.utc).isoformat(),
                    "Inhoud...",
                    "nl",
                    None,
                ),
            )
            await db.commit()

    async def _translate():
        from backend.services.polling import _translate_titles

        await _translate_titles()

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_setup())
        loop.run_until_complete(_translate())
    finally:
        loop.close()

    response = client.get("/articles")
    assert response.status_code == 200

    articles = response.json()
    article = [a for a in articles if a["url"] == "https://www.standaard.be/integration-test"][0]
    assert article["translated_title"] == "Translated Title"
