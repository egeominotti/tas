from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from bot.API.v0.StrategyBot.serializers import StrategyBotSerializer
from bot.models import StrategyBot


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


class StrategyBotList(ListAPIView):
    serializer_class = StrategyBotSerializer
    queryset = StrategyBot.objects.all().order_by('-created_at')


class StrategyBotCreate(CreateAPIView):
    serializer_class = StrategyBotSerializer
