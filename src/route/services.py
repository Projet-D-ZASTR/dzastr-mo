
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from config import get_db
from src.models.services import Service

router = APIRouter(prefix="/services", tags=["services"])


class ServiceCreate(BaseModel):
    Service_UserId: int
    Service_Name: str
    Service_PriceHour: float

    @field_validator("Service_Name")
    @classmethod
    def nom_non_vide(cls, v):
        if not v.strip():
            raise ValueError("Le label ne peut pas être vide")
        return v.strip()

    @field_validator("Service_PriceHour")
    @classmethod
    def prix_positif(cls, v):
        if v <= 0:
            raise ValueError("Le taux horaire doit être supérieur à 0")
        return v


class ServiceUpdate(BaseModel):
    Service_Name: str | None = None
    Service_PriceHour: float | None = None

    @field_validator("Service_Name")
    @classmethod
    def nom_non_vide(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Le label ne peut pas être vide")
        return v.strip() if v else v

    @field_validator("Service_PriceHour")
    @classmethod
    def prix_positif(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Le taux horaire doit être supérieur à 0")
        return v


class ServiceResponse(BaseModel):
    Service_Id: int
    Service_UserId: int
    Service_Name: str
    Service_PriceHour: float

    model_config = {"from_attributes": True}


@router.get("/", response_model=list[ServiceResponse])
def lister_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@router.get("/{service_id}", response_model=ServiceResponse)
def obtenir_service(service_id: int, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service introuvable")
    return service


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def creer_service(data: ServiceCreate, db: Session = Depends(get_db)):
    service = Service(
        Service_Name=data.Service_Name,
        Service_PriceHour=data.Service_PriceHour,
        Service_UserId=data.Service_UserId,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.put("/{service_id}", response_model=ServiceResponse)
def modifier_service(
        service_id: int, data: ServiceUpdate, db: Session = Depends(get_db)
):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service introuvable")
    if data.Service_Name is not None:
        service.Service_Name = data.Service_Name
    if data.Service_PriceHour is not None:
        service.Service_PriceHour = data.Service_PriceHour
    db.commit()
    db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_service(
        service_id: int, confirme: bool = False, db: Session = Depends(get_db)
):
    if not confirme:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ajoutez ?confirme=true pour confirmer la suppression",
        )
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service introuvable")
    db.delete(service)
    db.commit()
