from worker import celery

@celery.task(bind=True)
def test_task(self):
    return "working"