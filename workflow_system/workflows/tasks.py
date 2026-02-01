from celery import shared_task

@shared_task(bind=True,max_retries=3)
def send_workflow_notification(self, workflow_id):
    try:
        print(f"Sending notification for workflow {workflow_id}")
    except Exception as exc:
        raise self.retry(exc = exc, countdown = 10)