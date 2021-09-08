from django.core.management import BaseCommand
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'WebSocketStream Market Futures Binance'

    def handle(self, *args, **kwargs):
        pass
