from django.contrib import admin
from django.urls import include
from django.urls import path
from tas.views import index, websocket
from rest_framework.authtoken import views

urlpatterns = [
    path('', index),
    path('websocket/', websocket),
    path('', include('bot.urls')),
    path('', include('strategy.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('', include('analytics.urls')),
]
