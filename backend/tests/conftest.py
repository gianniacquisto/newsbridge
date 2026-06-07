import os
import tempfile

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

# Must set env before importing modules that use settings
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///test.db"


@pytest.fixture(scope="session")
def db_dir():
    """Create a temporary directory for the test database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{tmpdir}/newsbridge.db"
        yield tmpdir


@pytest_asyncio.fixture
async def client(db_dir):
    """Set up a test database and return a TestClient."""
    # Initialize the database schema and seed data
    from backend import database
    await database.init_db()

    # Create client with minimal app (no scheduler for tests)
    from main import app
    with TestClient(app) as test_client:
        yield test_client
