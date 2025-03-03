from settings.config import settings

celery_app = settings.celery_app.get_celery_app
