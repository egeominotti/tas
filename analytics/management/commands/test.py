from django.core.management import BaseCommand
import logging
from strategy.models import LogicEntry

logger = logging.getLogger('main')



class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):
        for k in LogicEntry.objects.all():
            print(k.content.html)
