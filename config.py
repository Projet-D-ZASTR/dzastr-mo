import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Hors conteneur Docker: priorise .env.local, sinon fallback .env.
if not os.path.exists("/.dockerenv"):
    if not load_dotenv(".env.local"):
        load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DB_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL/DB_URL is not set in environment")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
