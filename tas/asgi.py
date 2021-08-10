import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import bot.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tas.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AuthMiddlewareStack(
        URLRouter(
            bot.routing.websocket_urlpatterns
        )
    ),
})

