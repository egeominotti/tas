from rest_framework import serializers
from bot.models import StrategyBot

class StrategyBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyBot
        fields = ('name','time_frame','logic_entry','logic_exit','coins')
