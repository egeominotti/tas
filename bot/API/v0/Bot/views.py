from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from bot.API.v0.Bot.serializers import BotSerializer, BotCreateSerializer
from bot.models import Bot, UserExchange, BotLogger
from bot.model.bot import TradingBot
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
        bot = serializer.save()
        # usexg = UserExchange.objects.get(user=bot.user)
        # TradingBot(
        #     current_bot=bot,
        #     user=bot.user,
        #     userexchange=usexg,
        #     symbol=bot.coins.coins_taapi.symbol,
        #     symbol_exchange=bot.coins.coins_exchange.symbol,
        #     time_frame=bot.strategy.time_frame.time_frame,
        #     func_entry=bot.strategy.logic_entry,
        #     func_exit=bot.strategy.logic_exit,
        #     logger=BotLogger,
        #     bot_object=Bot,
        # )
