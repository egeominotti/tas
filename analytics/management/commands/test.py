from django.core.management import BaseCommand
import logging
from bot.models import BufferRecordData

logger = logging.getLogger('main')

def ciao():
    print("ciao")

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
       for k in BufferRecordData.objects.all():
           print(k)

