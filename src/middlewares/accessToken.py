from os import getenv

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

AUTH_SERVICE_URL = getenv("AUTH_SERVICE_URL", "http://localhost:8001/validate-token")
AUTH_SERVICE_TOKEN = getenv("AUTH_SERVICE_TOKEN")

if AUTH_SERVICE_TOKEN is None:
    raise RuntimeError("AUTH_SERVICE_TOKEN must be set in .env for access token verification to work")
if AUTH_SERVICE_URL is None:
    raise RuntimeError("AUTH_SERVICE_URL must be set in .env for access token verification to work")

async def verify_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    token = credentials.credentials 
    authorization = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                AUTH_SERVICE_URL,
                headers={
                    "Authorization": authorization,
                    "x-service-token": AUTH_SERVICE_TOKEN,
                }, 
                timeout=5.0,
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Auth service unavailable")

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    data = response.json()

    if not data.get("valid"):
        raise HTTPException(status_code=401, detail="Invalid token")

    return data["user"]