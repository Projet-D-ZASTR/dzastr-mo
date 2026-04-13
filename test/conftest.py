import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("AUTH_SERVICE_TOKEN", "test-token")
os.environ.setdefault("SERVICE_TOKEN", "test-token")
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from sqlalchemy import Column, Integer, String, create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from config import get_db  # noqa: E402
from main import app  # noqa: E402
from src.middlewares.accessToken import verify_user  # noqa: E402
from src.middlewares.servicetoken import verify_service_token  # noqa: E402
from src.models.base import Base  # noqa: E402
from src.models.client import (
    Client,  # noqa: E402, F401 — enregistre la table dans Base.metadata
)
from src.models.invoices import Invoice, InvoiceItem  # noqa: E402, F401
from src.models.services import Service  # noqa: E402, F401
from src.models.user_client import UserClient  # noqa: E402, F401


# Stub de la table users (appartient à dzastr-auth) — nécessaire pour résoudre la FK User_Id
class UserStub(Base):
    __tablename__ = "users"

    User_Id = Column(Integer, primary_key=True, autoincrement=True)
    User_Username = Column(String(80), nullable=False)
    User_Email = Column(String(80), nullable=False)


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
