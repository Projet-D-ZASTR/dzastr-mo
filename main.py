from contextlib import asynccontextmanager
from os import getenv

import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, FastAPI  # noqa: E402

from config import engine  # noqa: E402
from src.middlewares.accessToken import verify_user  # noqa: E402
from src.middlewares.servicetoken import verify_service_token  # noqa: E402
from src.models import (  # noqa: E402, F401 — needed for metadata
    Invoice,
    InvoiceItem,
    UserStub,
)
from src.models.base import Base  # noqa: E402
from src.route import client, serviceFacture, services  # noqa: E402
from src.route.invoices_route import router as invoices_router  # noqa: E402

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    send_default_pii=True,
    traces_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if engine.url.drivername != "sqlite":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    dependencies=[Depends(verify_service_token), Depends(verify_user)],
)

app.include_router(invoices_router)
app.include_router(services.router)
app.include_router(client.router)
app.include_router(serviceFacture.router)
