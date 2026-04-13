from dotenv import load_dotenv
load_dotenv()

from fastapi import Depends, FastAPI
from src.models.base import Base
from config import engine
from src.route import serviceFacture, services, client
from src.middlewares.servicetoken import verify_service_token
from src.middlewares.accessToken import verify_user

Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(verify_service_token), Depends(verify_user)])

app.include_router(services.router)
app.include_router(client.router)
app.include_router(serviceFacture.router)
