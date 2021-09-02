from rest_framework import serializers
from strategy.models import SymbolExchange


class CoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymbolExchange
        fields = '__all__'
