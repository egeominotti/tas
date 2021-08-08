from django.urls import path
from bot.API.v0.Bot.views import BotSpotList,BotFuturesList, BotCreate, BotUpdate, BotDestroy
from bot.API.v0.StrategyBot.views import StrategyBotList, StrategyBotCreate
from bot.API.v0.UserEchange.views import UserExchangeList, UserExchangeCreate
from bot.API.v0.BotLogger.views import BotLoggerList

urlpatterns = [

    path('api/v0/bot/futures/list', BotFuturesList.as_view()),
    path('api/v0/bot/spot/list', BotSpotList.as_view()),
    path('api/v0/bot/create', BotCreate.as_view()),
    path('api/v0/bot/update/<int:pk>', BotUpdate.as_view()),
    path('api/v0/bot/destroy/<int:pk>', BotDestroy.as_view()),

    path('api/v0/botlogger/list', BotLoggerList.as_view()),

    path('api/v0/strategybot/list', StrategyBotList.as_view()),
    path('api/v0/strategybot/create', StrategyBotCreate.as_view()),

    path('api/v0/userexhcange/list', UserExchangeList.as_view()),
    path('api/v0/userexhcange/create', UserExchangeCreate.as_view()),
]
