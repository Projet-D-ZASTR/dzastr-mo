from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from decimal import Decimal

from config import get_db
from src.models.serviceFacture import ServiceFacture

router = APIRouter(prefix="/service_facture", tags=["service_facture"])


class ServiceFactureCreate(BaseModel):
    ServiceFacture_Id: int
    Service_Id: int
    ServiceFacture_Lot: str

    @field_validator("ServiceFacture_Lot")
    @classmethod
    def service_facture_lot_non_vide(cls, v):
        if not v.strip():
            raise ValueError("Le ServiceFacture_Lot ne peut pas être vide")
        return v.strip()


class ServiceFactureUpdate(BaseModel):
    ServiceFacture_Id: int | None = None
    Service_Id: int | None = None
    ServiceFacture_Lot: str | None = None

    @field_validator("ServiceFacture_Lot")
    @classmethod
    def service_facture_lot_non_vide(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Le ServiceFacture_Lot ne peut pas être vide")
        return v.strip() if v else v


class ServiceFactureResponse(BaseModel):
    ServiceFacture_Id: int
    Service_Id: int
    ServiceFacture_Lot: str

    model_config = {"from_attributes": True}


@router.get("/", response_model=list[ServiceFactureResponse])
def lister_serviceFacture(db: Session = Depends(get_db)):
    return db.query(ServiceFacture).all()


@router.get("/{service_Id}", response_model=ServiceFactureResponse)
def obtenir_serviceFacture(service_Id: int, db: Session = Depends(get_db)):
    service = db.get(ServiceFacture, service_Id)
    if not service:
        raise HTTPException(status_code=404, detail="Service introuvable")
    return service


@router.post("/", response_model=ServiceFactureResponse, status_code=status.HTTP_201_CREATED)
def creer_serviceFacture(data: ServiceFactureCreate, db: Session = Depends(get_db)):
    service = ServiceFacture(
        ServiceFacture_Id=data.ServiceFacture_Id,
        Service_Id=data.Service_Id,
        ServiceFacture_Lot=data.ServiceFacture_Lot
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.delete("/{serviceFacture_Id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_serviceFacture(serviceFacture_Id: int, confirme: bool = False, db: Session = Depends(get_db)):
    if not confirme:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ajoutez ?confirme=true pour confirmer la suppression"
        )
    ServiceFacture = db.get(ServiceFacture, serviceFacture_Id)
    if not ServiceFacture:
        raise HTTPException(status_code=404, detail="Service introuvable")
    db.delete(ServiceFacture)
    db.commit()
