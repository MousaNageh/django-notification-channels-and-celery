from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_channel_notification.settings')

app = Celery('medicalDevices')
app.conf.enable_utc = False
app.conf.update(timezone='Africa/Cairo')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    "send-notifications-very-one-minute": {
        "task": "celery_channel_notification_app.tasks.send_periodic_notifiction",
        "schedule": crontab(minute="*/1"),
        # "args": (data1,data2),
    }
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

