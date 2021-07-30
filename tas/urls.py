from django.contrib import admin
from django.urls import path
from django.urls import path, include, re_path
from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('sentry-debug/', trigger_error),
    path('', include('analytics.urls')),
]
