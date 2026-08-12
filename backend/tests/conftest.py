from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


DB_PATH = Path(__file__).resolve().parents[1] / "db.sqlite3"


@pytest.fixture(autouse=True)
def reset_database():
    if DB_PATH.exists():
        DB_PATH.unlink()

    yield

    if DB_PATH.exists():
        DB_PATH.unlink()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client