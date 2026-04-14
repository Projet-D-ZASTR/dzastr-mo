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

    Facture_Id = Column(Integer, primary_key=True, autoincrement=True)
    User_Id = Column(Integer, nullable=False)
    Client_Id = Column(Integer, nullable=False)
    Facture_Prix = Column(Numeric(10, 2), nullable=False, default=0.00)
    Facture_Date = Column(Date, nullable=False)
    Facture_State = Column(
        SAEnum(InvoiceState), nullable=False, default=InvoiceState.draft
    )

    items = relationship(
        "InvoiceItem", back_populates="invoice", cascade="all, delete-orphan"
    )


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Facture_Id = Column(Integer, ForeignKey("invoices.Facture_Id"), nullable=False)
    Nombre_Id = Column(Integer, nullable=False)

    invoice = relationship("Invoice", back_populates="items")
