from celery import Celery
from config import REDIS_URL

# Create Celery app
celery = Celery(
    "processing",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Celery Configuration
celery.conf.update(
    task_track_started=True,
    result_expires=3600,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# 🔥 IMPORTANT FIX
# Explicitly include tasks module
celery.conf.imports = ("tasks",)