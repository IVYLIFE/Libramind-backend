from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models import IssuedBookModel


def get_due_soon_books(db: Session):
    today = date.today()
    cutoff = today + timedelta(days=5)

    return (
        db.query(IssuedBookModel)
        .filter(
            IssuedBookModel.returned_date.is_(None), IssuedBookModel.due_date <= cutoff
        )
        .all()
    )
