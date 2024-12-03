from celery import Celery

from app.core.config import get_config

config = get_config()


celery_app = Celery(
    "worker",
    backend=config.REDIS_URI,
    broker=config.REDIS_URI,
)

celery_app.conf.update(task_track_started=True)
