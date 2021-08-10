from bot.models import Bot
from djangochannelsrestframework import permissions
from bot.API.v0.Bot.serializers import BotSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
)


class BotConsumer(
    ListModelMixin,
    GenericAsyncAPIConsumer,
):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = (permissions.AllowAny,)
