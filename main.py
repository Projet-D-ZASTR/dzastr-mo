from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.models.base import Base
from config import engine
from src.route import services
from src.route import client

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(services.router)
app.include_router(client.router)
