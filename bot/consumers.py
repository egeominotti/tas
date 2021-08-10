from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from bot.models import Bot, UserExchange
from bot.API.v0.Bot.serializers import BotSerializer
from bot.API.v0.UserEchange.serializers import UserExchangeSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
)


class BotConsumer(GenericAsyncAPIConsumer, ObserverModelInstanceMixin):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class UserExchangeConsumer(
    ListModelMixin,
    GenericAsyncAPIConsumer,
):
    queryset = UserExchange.objects.all()
    serializer_class = UserExchangeSerializer
