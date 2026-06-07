import os
import tempfile

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient


@pytest_asyncio.fixture(scope="session")
async def db_dir():
    """Create a fresh temporary directory for the test session."""
    tmpdir = tempfile.mkdtemp()
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{tmpdir}/newsbridge.db"
    # Initialize the database schema and seed data
    from backend import database
    await database.init_db()
    yield tmpdir


@pytest_asyncio.fixture
async def client(db_dir):
    """Return a TestClient with the session database."""
    from main import app
    with TestClient(app) as test_client:
        yield test_client
