from django.urls import path
from exchange.API.v0.ExchangeList.views import ExchangeListView

urlpatterns = [
    path('api/v0/exchangelist/list', ExchangeListView.as_view()),
]
