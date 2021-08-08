from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import permissions
from bot.models import UserExchange
from bot.API.v0.UserEchange.serializers import UserExchangeSerializer

class BotConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = UserExchange.objects.all()
    serializer_class = UserExchangeSerializer
    #permission_classes = (permissions.AllowAny,)
