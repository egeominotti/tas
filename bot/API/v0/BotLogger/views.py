from rest_framework import generics
from bot.API.v0.BotLogger.serializers import BotLoggerSerializer
from bot.models import BotLogger
from rest_framework import authentication


class BotLoggerList(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BotLoggerSerializer
    queryset = BotLogger.objects.all().order_by('-created_at')

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
