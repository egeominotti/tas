from django.urls import path

from analytics.API.ByBt.views import ByBtRetrieve

urlpatterns = \
    [
        path('api/analytics/bybt/', ByBtRetrieve.as_view()),
    ]
