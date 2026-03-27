from datetime import date
from enum import StrEnum

from pydantic import BaseModel, model_validator


class InvoiceState(StrEnum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    cancelled = "cancelled"


class InvoiceCreate(BaseModel):
    user_id: int
    client_id: int
    invoice_price: float
    invoice_date: date
    item_ids: list[int]


class InvoiceUpdate(BaseModel):
    invoice_price: float | None = None
    invoice_date: date | None = None
    invoice_state: InvoiceState | None = None
    item_ids: list[int] | None = None


class InvoiceRead(BaseModel):
    invoice_id: int
    user_id: int
    client_id: int
    invoice_price: float
    invoice_date: date
    invoice_state: InvoiceState
    item_ids: list[int]

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
