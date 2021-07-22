from rest_framework import generics
from rest_framework.permissions import AllowAny
from analytics.API.ByBt.serializers import ByBtSerializer
from analytics.models import ByBt
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 288
    page_size_query_param = 'page_size'
    max_page_size = 288


class ByBtRetrieve(generics.ListAPIView):
    queryset = ByBt.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    serializer_class = ByBtSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol')
        return ByBt.objects \
            .filter(symbol=symbol,time=5).order_by('-created_at')
