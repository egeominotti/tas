from rest_framework import serializers
from bot.models import UserExchange

class UserExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExchange
        fields = '__all__'
