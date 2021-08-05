from rest_framework import serializers
from bot.models import Bot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('user', 'coins', 'strategy')
