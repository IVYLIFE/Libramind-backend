import smtplib
from email.message import EmailMessage
from app.database.config import settings

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


server = settings.SMTP_SERVER
port = settings.SMTP_PORT
user = settings.SMTP_USERNAME
password = settings.SMTP_PASSWORD
from_email = settings.SMTP_FROM_EMAIL


def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    # msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(body)
    # msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(server, port) as smtp:
            # smtp.starttls()
            smtp.login(user, password)
            smtp.send_message(msg)
            # smtp.sendmail(from_email, to_email, msg.as_string())

    except Exception as e:
        raise RuntimeError(f"Email send failed: {str(e)}")


