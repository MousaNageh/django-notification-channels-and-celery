
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask,CrontabSchedule
import json
# Create your models here.
class Notification(models.Model):
  message  = models.TextField()
  send_at = models.DateTimeField()
  def __str__(self) -> str:
      return self.message
  class Meta :
    ordering = ["-send_at"]

@receiver(post_save,sender=Notification)
def notification_handler(sender,instance,created,**kwargs):
  if created:
    schedule,created = CrontabSchedule.objects.get_or_create(
      hour=instance.send_at.hour,
      minute = instance.send_at.minute,
      day_of_month = instance.send_at.day,
      month_of_year=instance.send_at.month
      )
    task = PeriodicTask.objects.create(
      crontab=schedule,
      name="notification-very-specific-time"+str(instance.id),
      task="celery_channel_notification_app.tasks.send_notifiction_at_specific_time",
      args=json.dumps([instance.message])
      )
 
