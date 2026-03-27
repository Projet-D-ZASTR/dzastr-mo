import enum
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, model_validator


class InvoiceState(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    cancelled = "cancelled"


class InvoiceCreate(BaseModel):
    user_id: int
    client_id: int
    invoice_price: float
    invoice_date: date
    item_ids: List[int]


class InvoiceUpdate(BaseModel):
    invoice_price: Optional[float] = None
    invoice_date: Optional[date] = None
    invoice_state: Optional[InvoiceState] = None
    item_ids: Optional[List[int]] = None


class InvoiceRead(BaseModel):
    invoice_id: int
    user_id: int
    client_id: int
    invoice_price: float
    invoice_date: date
    invoice_state: InvoiceState
    item_ids: List[int]

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def extract_item_ids(cls, data):
        if hasattr(data, "items"):
            return {
                "invoice_id": data.invoice_id,
                "user_id": data.user_id,
                "client_id": data.client_id,
                "invoice_price": float(data.invoice_price),
                "invoice_date": data.invoice_date,
                "invoice_state": data.invoice_state,
                "item_ids": [item.item_id for item in data.items],
            }
        return data
