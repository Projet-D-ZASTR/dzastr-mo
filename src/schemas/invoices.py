from datetime import date
from enum import StrEnum

from pydantic import BaseModel, model_validator


class InvoiceState(StrEnum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    cancelled = "cancelled"


class InvoiceCreate(BaseModel):
    User_Id: int
    Client_Id: int
    Facture_Prix: float
    Facture_Date: date
    item_ids: list[int]


class InvoiceUpdate(BaseModel):
    Facture_Prix: float | None = None
    Facture_Date: date | None = None
    Facture_State: InvoiceState | None = None
    item_ids: list[int] | None = None


class InvoiceRead(BaseModel):
    Facture_Id: int
    User_Id: int
    Client_Id: int
    Facture_Prix: float
    Facture_Date: date
    Facture_State: InvoiceState
    item_ids: list[int]

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def extract_item_ids(cls, data):
        if hasattr(data, "items"):
            return {
                "Facture_Id": data.Facture_Id,
                "User_Id": data.User_Id,
                "Client_Id": data.Client_Id,
                "Facture_Prix": float(data.Facture_Prix),
                "Facture_Date": data.Facture_Date,
                "Facture_State": data.Facture_State,
                "item_ids": [item.Nombre_Id for item in data.items],
            }
        return data
