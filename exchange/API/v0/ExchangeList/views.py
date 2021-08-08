from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from exchange.API.v0.ExchangeList.serializers import ExchangeListSerializer
from exchange.models import ExchangeList
from rest_framework import authentication


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1


class ExchangeListView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = ExchangeListSerializer
    pagination_class = LargeResultsSetPagination
    queryset = ExchangeList.objects.all().order_by('-created_at')
