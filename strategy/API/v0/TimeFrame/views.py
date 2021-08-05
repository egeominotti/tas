from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from strategy.API.v0.TimeFrame.serializers import TimeFrameSerializer
from strategy.models import TimeFrame


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


class TimeFrameList(ListAPIView):
    serializer_class = TimeFrameSerializer
    queryset = TimeFrame.objects.all().order_by('-created_at')
