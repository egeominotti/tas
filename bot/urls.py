from django.urls import path
from bot.API.v0.Bot.views import BotList, BotCreate
from bot.API.v0.StrategyBot.views import StrategyBotList, StrategyBotCreate
from bot.API.v0.UserEchange.views import UserExchangeList, UserExchangeCreate

urlpatterns = [

    path('api/v0/bot/list', BotList.as_view()),
    path('api/v0/bot/create', BotCreate.as_view()),

    path('api/v0/strategybot/list', StrategyBotList.as_view()),
    path('api/v0/strategybot/create', StrategyBotCreate.as_view()),

    path('api/v0/userexhcange/list', UserExchangeList.as_view()),
    path('api/v0/userexhcange/create', UserExchangeCreate.as_view()),
]
