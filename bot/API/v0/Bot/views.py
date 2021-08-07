from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from bot.API.v0.Bot.serializers import BotSerializer, BotCreateSerializer, BotUpdateSerializer
from bot.models import Bot
from rest_framework import authentication


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1


class BotList(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BotSerializer
    pagination_class = LargeResultsSetPagination
    queryset = Bot.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')


class BotCreate(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BotCreateSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class BotUpdate(generics.UpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BotUpdateSerializer
    queryset = Bot.objects.all()



class BotDestroy(generics.DestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BotUpdateSerializer
    queryset = Bot.objects.all()
