"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from game.routing import websocket_urlpatterns
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from user.models import User
from django.db.models import F

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
my_timezone = timezone('Asia/Tashkent')
scheduler = BackgroundScheduler(time_zone=my_timezone)

def energy_increaser():
    User.objects.filter(energy__lt=F('energy_limit')).update(energy=F('energy') + 1, balance=F('balance') + F('bonus'))

scheduler.add_job(
    energy_increaser,
    trigger="interval",
    seconds=10
)
scheduler.start()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})
