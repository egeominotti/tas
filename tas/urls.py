from django.contrib import admin
from django.urls import path
from django.urls import path, include, re_path
from django.urls import path
from tas.views import index


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('analytics.urls')),
]
