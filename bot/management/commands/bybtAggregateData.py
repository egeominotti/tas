from django.core.management import BaseCommand
from analytics.models import ByBt
from datetime import datetime, timedelta
import datetime
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Calcola la media degli indici per 1H,2H,4H,8H,12H,24H'

    def handle(self, *args, **kwargs):
        pass
