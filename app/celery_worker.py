from celery import Celery
from app.database import settings

celery_app = Celery(
    "libramind",
    broker=settings.REDIS_URL,
    include=["app.tasks.remainder"]
)

celery_app.conf.task_routes = {
    "app.tasks.remainder.send_due_soon_reminder": {"queue": "emails"}
}
