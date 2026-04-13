
from fastapi import Depends, FastAPI  # noqa: E402

from config import engine  # noqa: E402
from src.middlewares.accessToken import verify_user  # noqa: E402
from src.middlewares.servicetoken import verify_service_token  # noqa: E402
from src.models import Invoice, InvoiceItem  # noqa: E402, F401 — needed for metadata
from src.models.base import Base  # noqa: E402
from src.route import client, serviceFacture, services  # noqa: E402
from src.route.invoices_route import router as invoices_router  # noqa: E402

Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(verify_service_token), Depends(verify_user)])

app.include_router(invoices_router)
app.include_router(services.router)
app.include_router(client.router)
app.include_router(serviceFacture.router)
