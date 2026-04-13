import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("AUTH_SERVICE_TOKEN", "test-token")
os.environ.setdefault("SERVICE_TOKEN", "test-token")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from config import get_db
from main import app
from src.middlewares.accessToken import verify_user
from src.middlewares.servicetoken import verify_service_token
from src.models.base import Base
from src.models.client import (
    Client,  # noqa: F401 — enregistre la table dans Base.metadata
)
from src.models.invoices import Invoice, InvoiceItem  # noqa: F401
from src.models.services import Service  # noqa: F401

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[verify_service_token] = lambda: None
    app.dependency_overrides[verify_user] = lambda: {"id": 1}
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
