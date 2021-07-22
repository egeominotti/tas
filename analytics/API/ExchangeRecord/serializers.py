from rest_framework import serializers
from analytics.models import ExchangeRecord


class ByBtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRecord
        fields = ('unix', 'created_at',)
        depth = 1
