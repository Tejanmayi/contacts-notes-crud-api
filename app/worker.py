from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "contact_notes",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Windows-specific configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_pool="solo",  # Use solo pool for Windows
    worker_max_tasks_per_child=1,
    broker_connection_retry_on_startup=True,
    task_ignore_result=True,
    task_store_errors_even_if_ignored=True,
)

@celery_app.task
def process_note_creation(note_id: int):
    """
    Background task to process newly created notes.
    This could include:
    - Indexing for search
    - Triggering analytics
    - Sending notifications
    - Enriching with additional data
    """
    # Simulate some processing time
    import time
    time.sleep(2)
    return {"status": "processed", "note_id": note_id} 