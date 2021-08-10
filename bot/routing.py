from django.urls import re_path
from bot.consumers import BotConsumer

websocket_urlpatterns = [
    re_path(r"^ws/bot/list$", BotConsumer.as_asgi()),
    re_path(r"^ws/userexchange/list$", BotConsumer.as_asgi()),
]
