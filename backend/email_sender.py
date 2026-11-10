import smtplib
import os
from pathlib import Path
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def enviar_correo(destino, pdf):
    required_settings = ("SMTP_SERVER", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD")
    missing_settings = [name for name in required_settings if not os.getenv(name)]
    if missing_settings:
        raise RuntimeError(
            "Faltan variables de configuración SMTP: " + ", ".join(missing_settings)
        )

    try:
        smtp_port = int(os.environ["SMTP_PORT"])
    except ValueError as exc:
        raise ValueError("SMTP_PORT debe ser un número entero entre 1 y 65535") from exc
    if not 1 <= smtp_port <= 65535:
        raise ValueError("SMTP_PORT debe ser un número entero entre 1 y 65535")

    msg = EmailMessage()
    msg["Subject"] = "Factura electrónica"
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = destino
    msg.set_content("Adjuntamos su factura.")
    with open(pdf, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=Path(pdf).name,
        )

    with smtplib.SMTP(os.environ["SMTP_SERVER"], smtp_port) as smtp:
        smtp.starttls()
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(msg)