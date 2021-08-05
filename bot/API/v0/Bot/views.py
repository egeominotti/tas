from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from bot.API.v0.Bot.serializers import BotSerializer
from bot.models import Bot


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


class BotList(generics.ListAPIView):
    serializer_class = BotSerializer
    queryset = Bot.objects.all().order_by('-created_at')

class BotCreate(generics.CreateAPIView):
    serializer_class = BotSerializer
    queryset = Bot.objects.all().order_by('-created_at')
