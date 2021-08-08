from rest_framework import serializers
from bot.models import Bot


class BotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('coins', 'strategy', 'market_futures', 'market_spot', 'leverage', 'amount')


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'
        depth = 2


class BotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'
