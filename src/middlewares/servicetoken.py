import os

from fastapi import Header, HTTPException


def verify_service_token(x_token: str = Header(...)):
    EXPECTED_TOKEN = os.getenv("SERVICE_TOKEN")
    if EXPECTED_TOKEN is None:
        raise HTTPException(status_code=500, detail="Service token not configured in .env")
    if x_token != EXPECTED_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid service token")
