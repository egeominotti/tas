from django.core.management import BaseCommand
import logging
from bot.services.indicator import RealTimeIndicator

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Valori real time delle candele'

    def handle(self, *args, **kwargs):

        indicator = RealTimeIndicator('RVNUSDT', '15m')
        print(indicator.ema(5))
        print(indicator.rsi(14))
        print(indicator.bbands(20))
        print(indicator.candle())
