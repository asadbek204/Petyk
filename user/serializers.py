from rest_framework.serializers import ModelSerializer
from .models import User, Harem


class UserSerializer(ModelSerializer):
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
