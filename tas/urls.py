from django.contrib import admin
from django.urls import include
from django.urls import path
from tas.views import index

urlpatterns = [
    path('', index),
    path('', include('bot.urls')),
    path('', include('strategy.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('analytics.urls')),
]
