from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import get_db
from src.models.invoices import Invoice, InvoiceItem
from src.schemas.invoices import InvoiceCreate, InvoiceRead, InvoiceUpdate

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    invoice = Invoice(
        user_id=payload.user_id,
        client_id=payload.client_id,
        invoice_price=payload.invoice_price,
        invoice_date=payload.invoice_date,
    )
    db.add(invoice)
    db.flush()

    for item_id in payload.item_ids:
        db.add(InvoiceItem(invoice_id=invoice.invoice_id, item_id=item_id))

    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/", response_model=list[InvoiceRead])
def list_invoices(user_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Invoice)
    if user_id is not None:
        query = query.filter(Invoice.user_id == user_id)
    return query.all()


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
        )
    return invoice


@router.put("/{invoice_id}", response_model=InvoiceRead)
def update_invoice(
    invoice_id: int, payload: InvoiceUpdate, db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
        )

    if payload.invoice_price is not None:
        invoice.invoice_price = payload.invoice_price
    if payload.invoice_date is not None:
        invoice.invoice_date = payload.invoice_date
    if payload.invoice_state is not None:
        invoice.invoice_state = payload.invoice_state

    if payload.item_ids is not None:
        for item in invoice.items:
            db.delete(item)
        db.flush()
        for item_id in payload.item_ids:
            db.add(InvoiceItem(invoice_id=invoice.invoice_id, item_id=item_id))

    db.commit()
    db.refresh(invoice)
    return invoice


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found"
        )
    db.delete(invoice)
    db.commit()
