from rest_framework import serializers
from analytics.models import ByBt


class ByBtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ByBt
        fields = ('longShortRateListLast', 'created_at',)
        depth = 1
