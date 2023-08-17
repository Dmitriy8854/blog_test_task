import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
app = Celery("blog")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task
def hello(invoice_id):
    return "hello world"


app.conf.beat_schedule = {
    "send_1_day": {
        "task": "api.tasks.post_send",
        "schedule": crontab(hour="*/24"),
    },
}

# app.conf.beat_schedule = {"se-seconds": {"task": "tasks.check", "schedule": 100.0}}


# http://lexover.ru/2021/02/04/celery-periodic-tasks/
