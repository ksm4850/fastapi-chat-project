from app.celery_task import celery_app


@celery_app.task
def log():
    return "log"
