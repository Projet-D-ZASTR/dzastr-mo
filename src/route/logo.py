from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from config import get_db
from src.middlewares.accessToken import verify_user
from src.models.logo import Logo

router = APIRouter(prefix="/logos", tags=["logos"])

ALLOWED_TYPES = {"image/png", "image/jpeg", "image/webp", "image/svg+xml"}
MAX_SIZE = 2 * 1024 * 1024  # 2 MB


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_logo(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_user),
):
    user_id = current_user["User_Id"]

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté. Acceptés : {', '.join(ALLOWED_TYPES)}",
        )

    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(
            status_code=400, detail="Fichier trop volumineux (max 2 Mo)"
        )

    existing = db.query(Logo).filter(Logo.User_Id == user_id).first()
    if existing:
        existing.Logo_Data = data
        existing.Logo_Filename = file.filename
        existing.Logo_Sizebytes = len(data)
        db.commit()
        db.refresh(existing)
        return {"Logo_Id": existing.Logo_Id, "Logo_Filename": existing.Logo_Filename}

    logo = Logo(
        User_Id=user_id,
        Logo_Data=data,
        Logo_Filename=file.filename,
        Logo_Sizebytes=len(data),
    )
    db.add(logo)
    db.commit()
    db.refresh(logo)
    return {"Logo_Id": logo.Logo_Id, "Logo_Filename": logo.Logo_Filename}


@router.get("/me")
def get_logo(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_user),
):
    user_id = current_user["User_Id"]
    logo = db.query(Logo).filter(Logo.User_Id == user_id).first()
    if not logo:
        raise HTTPException(status_code=404, detail="Logo introuvable")
    return Response(
        content=logo.Logo_Data,
        media_type="image/png",
        headers={"Content-Disposition": f"inline; filename={logo.Logo_Filename}"},
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_logo(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_user),
):
    user_id = current_user["User_Id"]
    logo = db.query(Logo).filter(Logo.User_Id == user_id).first()
    if not logo:
        raise HTTPException(status_code=404, detail="Logo introuvable")
    db.delete(logo)
    db.commit()
