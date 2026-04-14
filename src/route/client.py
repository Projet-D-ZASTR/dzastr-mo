import csv
import io

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from config import get_db
from src.middlewares.accessToken import verify_user
from src.models.client import Client

router = APIRouter(prefix="/clients", tags=["clients"])


class ClientCreate(BaseModel):
    user_id: int
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
    Client_Id: int
    User_Id: int
    Client_Name: str
    Client_Entreprise: str
    Client_Email: str
    Client_Address: str

    model_config = {"from_attributes": True}


@router.get("/export/csv", response_class=StreamingResponse)
async def exporter_clients_csv(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_user),
):
    user_id = current_user["User_Id"]
    clients = db.query(Client).filter(Client.User_Id == user_id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Client_Id", "User_Id", "Nom", "Entreprise", "Email", "Adresse"])
    for c in clients:
        writer.writerow(
            [
                c.Client_Id,
                c.User_Id,
                c.Client_Name,
                c.Client_Entreprise,
                c.Client_Email,
                c.Client_Address,
            ]
        )
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=clients.csv"},
    )


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
        User_Id=data.user_id,
        Client_Name=data.name,
        Client_Entreprise=data.entreprise,
        Client_Email=data.email,
        Client_Address=data.adresse,
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
        client.Client_Name = data.name
    if data.entreprise is not None:
        client.Client_Entreprise = data.entreprise
    if data.email is not None:
        client.Client_Email = data.email
    if data.adresse is not None:
        client.Client_Address = data.adresse
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
