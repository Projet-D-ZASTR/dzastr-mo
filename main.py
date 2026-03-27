from fastapi import FastAPI
from src.models.base import Base
from src.models import Invoice, InvoiceItem  # noqa: F401 — needed for metadata
from src.route.invoices_route import router as invoices_router
from config import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(invoices_router)
