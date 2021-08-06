from rest_framework import serializers
from bot.models import StrategyBot


class StrategyBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyBot
        fields = ('id', 'name',)
