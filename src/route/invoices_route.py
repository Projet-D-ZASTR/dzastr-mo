from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import get_db
from src.models.invoices import Invoice, InvoiceItem
from src.schemas.invoices import InvoiceCreate, InvoiceRead, InvoiceUpdate

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    invoice = Invoice(
        User_Id=payload.User_Id,
        Client_Id=payload.Client_Id,
        Facture_Prix=payload.Facture_Prix,
        Facture_Date=payload.Facture_Date,
    )
    db.add(invoice)
    db.flush()

    for nombre_id in payload.item_ids:
        db.add(InvoiceItem(Facture_Id=invoice.Facture_Id, Nombre_Id=nombre_id))

    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/", response_model=list[InvoiceRead])
def list_invoices(User_Id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Invoice)
    if User_Id is not None:
        query = query.filter(Invoice.User_Id == User_Id)
    return query.all()


@router.get("/{facture_id}", response_model=InvoiceRead)
def get_invoice(facture_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.Facture_Id == facture_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
        )
    return invoice


@router.put("/{facture_id}", response_model=InvoiceRead)
def update_invoice(
    facture_id: int, payload: InvoiceUpdate, db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(Invoice.Facture_Id == facture_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
        )

    if payload.Facture_Prix is not None:
        invoice.Facture_Prix = payload.Facture_Prix
    if payload.Facture_Date is not None:
        invoice.Facture_Date = payload.Facture_Date
    if payload.Facture_State is not None:
        invoice.Facture_State = payload.Facture_State

    if payload.item_ids is not None:
        for item in invoice.items:
            db.delete(item)
        db.flush()
        for nombre_id in payload.item_ids:
            db.add(InvoiceItem(Facture_Id=invoice.Facture_Id, Nombre_Id=nombre_id))

    db.commit()
    db.refresh(invoice)
    return invoice


@router.delete("/{facture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(facture_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.Facture_Id == facture_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
        )
    db.delete(invoice)
    db.commit()
