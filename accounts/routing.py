from django.urls import path
from .consumers import CameraFeedConsumer

websocket_urlpatterns = [
    path('ws/camera/', CameraFeedConsumer.as_asgi()),
]