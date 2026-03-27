from fastapi import FastAPI
from src.models.base import Base
from config import engine
from src.route import services

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(services.router)
