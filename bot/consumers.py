from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import permissions
from bot.models import Bot
from bot.API.v0.Bot.serializers import BotSerializer

class BotConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = (permissions.AllowAny,)
