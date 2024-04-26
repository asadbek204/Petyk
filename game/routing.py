from django.urls import re_path
from .consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r"user/ws/game/$", GameConsumer.as_asgi()),
]
