from enum import StrEnum

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from .base import Base


class InvoiceState(StrEnum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    cancelled = "cancelled"


class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    client_id = Column(Integer, nullable=False)
    invoice_price = Column(Numeric(10, 2), nullable=False, default=0.00)
    invoice_date = Column(Date, nullable=False)
    invoice_state = Column(
        SAEnum(InvoiceState), nullable=False, default=InvoiceState.draft
    )

    items = relationship(
        "InvoiceItem", back_populates="invoice", cascade="all, delete-orphan"
    )


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey("invoices.invoice_id"), nullable=False)
    item_id = Column(Integer, nullable=False)

    invoice = relationship("Invoice", back_populates="items")
