from rest_framework import serializers
from bot.models import Bot

class BotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('coins','strategy')

class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'
        depth = 2
