import smtplib
from celery import shared_task
from email.mime.text import MIMEText

from app.database import settings


@shared_task(bind=True, max_retries=3)
def send_due_soon_reminder(self, to_email: str, subject: str, body: str):
    try:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, [to_email], msg.as_string())
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
