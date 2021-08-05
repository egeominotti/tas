from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from bot.API.v0.Bot.serializers import BotSerializer
from bot.models import Bot, UserExchange, BotLogger
from bot.model.bot import TradingBot


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

    def perform_create(self, serializer):
        bot = serializer.save()
        usexg = UserExchange.objects.get(user=bot.user)
        TradingBot(
            current_bot=bot,
            user=bot.user,
            userexchange=usexg,
            symbol=bot.coins.coins_taapi.symbol,
            symbol_exchange=bot.coins.coins_exchange.symbol,
            time_frame=bot.strategy.time_frame.time_frame,
            func_entry=bot.strategy.logic_entry,
            func_exit=bot.strategy.logic_exit,
            logger=BotLogger,
            bot_object=Bot
        )
