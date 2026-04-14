from contextlib import asynccontextmanager
from os import getenv

import sentry_sdk
from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from config import engine
from src.middlewares.accessToken import verify_user
from src.middlewares.servicetoken import verify_service_token
from src.models import Invoice, InvoiceItem, UserStub
from src.models.base import Base
from src.route import client, serviceFacture, services
from src.route.invoices_route import router as invoices_router
from src.route.sendEmailRoute import router as sendEmailRoute

load_dotenv()

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
app.include_router(sendEmailRoute)