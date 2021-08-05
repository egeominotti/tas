from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from strategy.API.v0.Coins.serializers import CoinsSerializer
from bot.models import Coins


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


class CoinsList(generics.ListAPIView):
    serializer_class = CoinsSerializer
    queryset = Coins.objects.all().order_by('-created_at')
