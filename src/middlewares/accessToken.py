from os import getenv

from fastapi import Header, HTTPException, Depends
import httpx

AUTH_SERVICE_URL = getenv("AUTH_SERVICE_URL", "http://localhost:8001/validate-token")
SERVICE_TOKEN = getenv("AUTH_SERVICE_TOKEN")


async def verify_user(
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                AUTH_SERVICE_URL,
                headers={
                    "Authorization": authorization,
                    "x-service-token": SERVICE_TOKEN,
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

    return data["user"]  # 👈 useful for downstream routes