from os import getenv
import smtplib
from email.message import EmailMessage


def send_email(
    to: list[str],
    cc: list[str],
    bcc: list[str],
    subject: str,
    message: str,
    pdf_bytes: bytes,
    pdf_filename: str,
):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = getenv("SMTP_EMAIL_FROM")
    msg["To"] = ", ".join(to)

    if cc:
        msg["Cc"] = ", ".join(cc)

    # Important: SMTP needs ALL recipients here
    all_recipients = to + cc + bcc

    msg.set_content(message)

    # Attach PDF
    msg.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename=pdf_filename,
    )

    with smtplib.SMTP(getenv("SMTP_SERVER"), int(getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(getenv("SMTP_USERNAME"), getenv("SMTP_PASSWORD"))
        server.send_message(msg, to_addrs=all_recipients)
