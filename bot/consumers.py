from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import permissions
from bot.models import UserExchange
from bot.API.v0.UserEchange.serializers import UserExchangeCreateSerializer

class BotConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = UserExchange.objects.all()
    serializer_class = UserExchangeCreateSerializer
    permission_classes = (permissions.AllowAny,)