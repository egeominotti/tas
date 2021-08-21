from django.core.management import BaseCommand
import logging
from bot.services.indicator import Indicator

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Test'

    def handle(self, *args, **kwargs):
        indicator = Indicator('RVNUSDT','5m', True)
        print(indicator.ema(5))
        print(indicator.rsi(14))
        print(indicator.bbands(20))
        print(indicator.candle())
