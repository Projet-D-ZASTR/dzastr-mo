from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from config import get_db
from src.models.client import Client

router = APIRouter(prefix="/clients", tags=["clients"])


class ClientCreate(BaseModel):
    name: str
    entreprise: str
    email: str
    adresse: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("entreprise")
    @classmethod
    def entreprise_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Entreprise cannot be empty")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Email cannot be empty")
        return v.strip()

    @field_validator("adresse")
    @classmethod
    def adresse_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Address cannot be empty")
        return v.strip()


class ClientUpdate(BaseModel):
    name: str | None = None
    entreprise: str | None = None
    email: str | None = None
    adresse: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip() if v else v

    @field_validator("entreprise")
    @classmethod
    def entreprise_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Entreprise cannot be empty")
        return v.strip() if v else v

    @field_validator("email")
    @classmethod
    def email_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Email cannot be empty")
        return v.strip() if v else v

    @field_validator("adresse")
    @classmethod
    def adresse_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Address cannot be empty")
        return v.strip() if v else v


class ClientResponse(BaseModel):
    id: int
    name: str
    entreprise: str
    email: str
    adresse: str

    model_config = {"from_attributes": True}


@router.get("/", response_model=list[ClientResponse])
def lister_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.get("/{client_id}", response_model=ClientResponse)
def obtenir_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def creer_client(data: ClientCreate, db: Session = Depends(get_db)):
    client = Client(
        name=data.name,
        entreprise=data.entreprise,
        email=data.email,
        adresse=data.adresse,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.put("/{client_id}", response_model=ClientResponse)
def modifier_client(client_id: int, data: ClientUpdate, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if data.name is not None:
        client.name = data.name
    if data.entreprise is not None:
        client.entreprise = data.entreprise
    if data.email is not None:
        client.email = data.email
    if data.adresse is not None:
        client.adresse = data.adresse
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_client(
    client_id: int, confirme: bool = False, db: Session = Depends(get_db)
):
    if not confirme:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Add ?confirme=true to delete",
        )
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
