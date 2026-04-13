from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import get_db
from src.models.client import Client
from src.models.user_client import UserClient

router = APIRouter(prefix="/user-clients", tags=["user-clients"])


class UserClientCreate(BaseModel):
    User_Id: int
    Client_Id: int


class UserClientResponse(BaseModel):
    id: int
    User_Id: int
    Client_Id: int

    model_config = {"from_attributes": True}


@router.post(
    "/", response_model=UserClientResponse, status_code=status.HTTP_201_CREATED
)
def lier_user_client(data: UserClientCreate, db: Session = Depends(get_db)):
    if not db.get(Client, data.Client_Id):
        raise HTTPException(status_code=404, detail="Client not found")
    existe = (
        db.query(UserClient)
        .filter_by(User_Id=data.User_Id, Client_Id=data.Client_Id)
        .first()
    )
    if existe:
        raise HTTPException(status_code=409, detail="Liaison already exists")
    liaison = UserClient(User_Id=data.User_Id, Client_Id=data.Client_Id)
    db.add(liaison)
    db.commit()
    db.refresh(liaison)
    return liaison


@router.get("/{user_id}", response_model=list[UserClientResponse])
def clients_par_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(UserClient).filter_by(User_Id=user_id).all()


@router.get("/client/{client_id}", response_model=list[UserClientResponse])
def users_par_client(client_id: int, db: Session = Depends(get_db)):
    return db.query(UserClient).filter_by(Client_Id=client_id).all()


@router.delete("/{user_id}/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delier_user_client(user_id: int, client_id: int, db: Session = Depends(get_db)):
    liaison = (
        db.query(UserClient).filter_by(User_Id=user_id, Client_Id=client_id).first()
    )
    if not liaison:
        raise HTTPException(status_code=404, detail="Liaison not found")
    db.delete(liaison)
    db.commit()
