from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .models import User, Harem
from .serializers import UserSerializer, HaremSerializer, HaremInSerializer


def page(request):
    return render(request, 'index.html')


@api_view(http_method_names=['get'])
def get_friends(request: Request, id: int):
    friends = User.objects.filter(refered_by=id)
    return Response(UserSerializer(friends, many=True).data)


@api_view(http_method_names=['post'])
def create_harem(request: Request, id: int):
    try:
        user = User.objects.get(user_id=int(id))
    except User.DoesNotExist:
        return Response(status=404, data={'detail': 'user not found'})
    request.data.update(owner=int(id))
    print(request.data)
    harem = HaremInSerializer(data=request.data)
    if harem.is_valid():
        harem.save()
        return Response({'message': 'success'})
    else:
        return Response(status=400, data={'detail': {'errors': harem.errors, 'error_messages': harem.error_messages}})


@api_view(http_method_names=['get'])
def get_harem(request: Request, name: str):
    try:
        harem = Harem.objects.get(name=name)
    except Harem.DoesNotExist:
        return Response(HaremSerializer(harem).data)
    else:
        return Response(status=404, data={'detail': f'harem not with name {name} found'})


@api_view(http_method_names=['post'])
def join_harem(request: Request, id: int):
    try:
        user = User.objects.get(user_id=int(id))
    except User.DoesNotExist:
        return Response(status=404, data={'detail': 'user not found'})
    try:
        harem = Harem.objects.get(name=request.data.get('name'))
    except Harem.DoesNotExist:
        return Response(status=404, data={'detail': 'haren not found'})
    harem.members.add(user)
    return Response(data={'message': 'success'})


@api_view(http_method_names=['delete'])
def delete_harem(request: Request, id: int, name: str, password: str):
    try:
        harem = Harem.objects.get(name=name)
    except Harem.DoesNotExist:
        return Response(status=404, data={'detail': 'harem not found'})
    if not harem.validate_key(password):
        return Response(status=403, data={'detail': 'incorrect password'})
    harem.delete()
    return Response(data={'message': 'harem deleted'})


@api_view(http_method_names=['delete'])
def leave_harem(request: Request, id: int, name: str):
    try:
        user = User.objects.get(user_id=id)
    except User.DoesNotExist:
        return Response(status=404, data={'detail': "user not found"})
    try:
        harem = Harem.objects.get(name=name)
    except Harem.DoesNotExist:
        return Response(status=404, data={'detail': 'harem not found'})
    if user not in harem.members.all():
        return Response(status=404, data={'detail': 'user is not a member of harem'})
    harem.members.remove(user)
    return Response(HaremSerializer(harem).data)

@api_view(http_method_names=['get'])
def get_statistics(request: Request):
    return Response(data=UserSerializer(User.objects.all()[100], many=True).data)
