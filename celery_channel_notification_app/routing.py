from django.urls import path

from .consumers import NotificationConsumer

urls = [
    path('ws/notification',
        NotificationConsumer.as_asgi()),
]