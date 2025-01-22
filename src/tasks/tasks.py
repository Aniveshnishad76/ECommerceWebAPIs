"""
Celery worker tasks definition
"""
from src.tasks.celery import celery_master_app

celery_master_app.autodiscover_tasks()
celery_master_app.conf.timezone = "IST"

celery_master_app.conf.beat_schedule = {}