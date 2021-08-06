from rest_framework import generics
from bot.API.v0.BotLogger.serializers import BotLoggerSerializer
from bot.models import BotLogger


class BotLoggerList(generics.ListAPIView):
    serializer_class = BotLoggerSerializer
    queryset = BotLogger.objects.all().order_by('-created_at')
