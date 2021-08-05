import asyncio
from django.core.management import BaseCommand
from asgiref.sync import sync_to_async
import logging
from bot.models import BufferStreamWebSocket
from multiprocessing import Process
import multiprocessing

logger = logging.getLogger('main')

def ciao():
    print("ciao")

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        print("Number of cpu : ", multiprocessing.cpu_count())

        p = Process(target=ciao)
        p.start()
        p.join()

