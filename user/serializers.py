from rest_framework.serializers import ModelSerializer
from .models import User, Harem
from market.serializers import ButtonSerializer

class UserSerializer(ModelSerializer):
    button = ButtonSerializer()
    class Meta:
        model = User
        fields = '__all__'


class HaremSerializer(ModelSerializer):
    class Meta:
        model = Harem
        fields = '__all__'


class HaremInSerializer(ModelSerializer):
    class Meta:
        model = Harem
        fields = ['key', 'name', 'target', 'owner']
