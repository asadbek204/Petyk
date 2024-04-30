from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Channel, Button
from user.models import User
from .serializers import ChannelSerializer, ButtonSerializer


@api_view(http_method_names=['get'])
def get_tasks(request: Request, id: int):
    channel = Channel.objects.all()
    # filter using api from bot or any thing else
    return Response(data=ChannelSerializer(channel, many=True).data)


@api_view(http_method_names=['get'])
def get_boosts(request: Request, id: int, extra: str):
    buttons = []
    if extra == 'my':
        buttons = Button.objects.filter(users=id)
    else:
        buttons = Button.objects.exclude(users=id)
    return Response(data=ButtonSerializer(buttons, many=True).data)


@api_view(http_method_names=['get'])
def get_boost(request: Request, id: int, name: str):
    try:
        button = Button.objects.get(name=name)
    except Button.DoesNotExist:
        return Response(status=404, data={'detail': 'button not found'})
    return Response(data=ButtonSerializer(button).data)


@api_view(http_method_names=['get'])
def buy_boost(request: Request, id: int, name: str):
    try:
        user = User.objects.get(user_id=id)
    except User.DoesNotExist:
        return Response(status=404, data={'detail': 'usser not found'})
    try:
        button = Button.objects.get(name=name)
    except Button.DoesNotExist:
        return Response(status=404, data={'detail': 'button not found'})
    button.users.add(user)
    user.balance -= button.price
    user.bonus = button.bonus
    user.tap_step = button.tap_step
    user.level = button.level
    user.button = button
    user.save()
    return Response(data={'message': 'success'})
