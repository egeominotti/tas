import asyncio
from django.core.management import BaseCommand
from asgiref.sync import sync_to_async
import logging
from bot.models import BufferStreamWebSocket

logger = logging.getLogger('main')


@sync_to_async
def get_users():
    BufferStreamWebSocket.objects.all()

async def user_loop():
    results = await get_users()
    print(results)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(user_loop())
