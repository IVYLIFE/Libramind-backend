from datetime import date
from app.database import get_db
from app.tasks import send_due_soon_reminder
from app.services.overdue import get_due_soon_books
from app.templates import generate_remainder_email

def send_daily_remainder():
    db = get_db()
    books = get_due_soon_books(db)

    for issued in books:
        student = issued.student
        book = issued.book
        days_remaining = (issued.due_date - date.today()).days

        subject, body = generate_remainder_email(
            student_name=student.name,
            book_title=book.title,
            due_date=str(issued.due_date),
            days_remaining=days_remaining
        )

        send_due_soon_reminder.delay(
            to_email=student.email,
            subject=subject,
            body=body
        )
