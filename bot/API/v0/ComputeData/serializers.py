from rest_framework import serializers
from bot.models import ComputedData


class ComputedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputedData
        fields = '__all__'
