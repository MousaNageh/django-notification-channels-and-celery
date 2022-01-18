from celery import shared_task 
from asgiref.sync import async_to_sync 
from channels.layers import get_channel_layer
@shared_task(bind=True)
def send_periodic_notifiction(self):
  channel = get_channel_layer()
  async_to_sync(channel.group_send)("broadcast_notifications",
                                    {
                                        "type": "websocket.message",
                                        "message": "this is  hard coded periodic tasks every one minute",
                                    }
                                    )
  return "Done"

@shared_task(bind=True)
def send_notifiction_at_specific_time(self,data):
  channel = get_channel_layer()
  async_to_sync(channel.group_send)("broadcast_notifications",
                                    {
                                        "type": "websocket.message",
                                        "message": f"{data}",
                                    }
                                    )
  return "Done"

