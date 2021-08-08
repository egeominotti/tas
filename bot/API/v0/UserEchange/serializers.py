from rest_framework import serializers
from bot.models import UserExchange


class UserExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExchange
        fields = '__all__'
        depth = 1


class UserExchangeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExchange
        fields = ('exchange', 'api_key', 'api_secret','live')
