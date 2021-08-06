from rest_framework import serializers
from bot.models import BotLogger


class BotLoggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotLogger
        fields = '__all__'
