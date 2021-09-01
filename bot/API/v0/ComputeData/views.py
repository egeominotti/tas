from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from bot.API.v0.ComputeData.serializers import ComputedDataSerializer
from bot.models import ComputedData
from rest_framework import authentication


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1


class ComputedDataList(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = ComputedDataSerializer
    pagination_class = LargeResultsSetPagination
    queryset = ComputedData.objects.all()
