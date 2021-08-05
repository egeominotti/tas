from django.urls import path
from strategy.API.v0.Coins.views import CoinsList
from strategy.API.v0.TimeFrame.views import TimeFrameList

urlpatterns = [
    path('api/v0/coins/list', CoinsList.as_view()),
    path('api/v0/timeframe/list', TimeFrameList.as_view()),
]
