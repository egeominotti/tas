import asyncio
from django.core.management import BaseCommand
from asgiref.sync import sync_to_async
import logging
from bot.models import BufferStreamWebSocket
from multiprocessing import Process
import multiprocessing
from bot.models import UserExchange

logger = logging.getLogger('main')

def ciao():
    print("ciao")

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        for k in UserExchange.objects.all():
            k.flgEnable = False
            k.save()

