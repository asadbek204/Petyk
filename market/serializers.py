from rest_framework.serializers import ModelSerializer
from .models import Channel, Button


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fileds = '__all__'


class ButtonSerializer(ModelSerializer):
    class Meta:
        model = Button
        fields = '__all__'
