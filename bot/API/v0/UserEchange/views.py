from rest_framework import authentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from bot.API.v0.UserEchange.serializers import UserExchangeSerializer, UserExchangeCreateSerializer
from bot.models import UserExchange


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


class UserExchangeList(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = UserExchangeSerializer
    queryset = UserExchange.objects.all().order_by('-created_at')

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')


class UserExchangeCreate(CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = UserExchangeCreateSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
