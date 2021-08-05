from rest_framework import serializers
from strategy.models import Coins


class CoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins
        fields = '__all__'
        depth = 1
