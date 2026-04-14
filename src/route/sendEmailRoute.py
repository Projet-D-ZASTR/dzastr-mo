from fastapi import APIRouter, File, Form, UploadFile, status
from typing import List
import src.services.emailService as email_service
from os import getenv

router = APIRouter(prefix="/send-email/", tags=["email"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_email_route(
    to: List[str] = Form(...),
    cc: List[str] = Form([]),
    bcc: List[str] = Form([]),
    subject: str = Form(...),
    message: str = Form(...),
    pdf: UploadFile = File(...),
):
    pdf_bytes = await pdf.read()

    email_service.send_email(
        smtp_server=getenv("SMTP_SERVER"),
        smtp_port=getenv("SMTP_PORT"),
        username=getenv("SMTP_USERNAME"),
        password=getenv("SMTP_PASSWORD"),
        to=to,
        cc=cc,
        bcc=bcc,
        subject=subject,
        message=message,
        pdf_bytes=pdf_bytes,
        pdf_filename=pdf.filename,
    )

    return {"status": "email sent"}