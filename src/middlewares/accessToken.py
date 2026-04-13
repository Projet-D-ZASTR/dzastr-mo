from os import getenv

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

AUTH_SERVICE_URL = getenv("AUTH_SERVICE_URL", "http://dzaster-auth:8081")
AUTH_SERVICE_TOKEN = getenv("AUTH_SERVICE_TOKEN")

if AUTH_SERVICE_TOKEN is None:
    raise RuntimeError(
        "AUTH_SERVICE_TOKEN must be set in .env for access token verification to work"
    )
VERIFY_PATH = "/api/secure/verify"


def build_verify_url(raw_url: str) -> str:
    base_url = raw_url.strip().rstrip("/")
    if not base_url.startswith(("http://", "https://")):
        base_url = f"https://{base_url}"
    return f"{base_url}{VERIFY_PATH}"


async def verify_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    token = credentials.credentials
    authorization = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        try:
            verify_url = build_verify_url(AUTH_SERVICE_URL)
            response = await client.get(
                verify_url,
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
