from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.models.base import Base
from src.models import Invoice, InvoiceItem  # noqa: F401 — needed for metadata
from src.route.invoices_route import router as invoices_router
from config import engine
from src.route import serviceFacture, services, client

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(invoices_router)
app.include_router(services.router)
app.include_router(client.router)
app.include_router(serviceFacture.router)
