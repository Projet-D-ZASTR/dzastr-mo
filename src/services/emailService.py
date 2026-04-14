import smtplib
from email.message import EmailMessage

def send_email(
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
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
    msg["From"] = username
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

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg, to_addrs=all_recipients)