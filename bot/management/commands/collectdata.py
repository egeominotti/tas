from django.core.management import BaseCommand
import logging
from bot.services.indicator import RealTimeIndicator

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Bot che scarica il bilancio di ogni utente e lo salva nel sistema ogni 15 secondi'

    def handle(self, *args, **kwargs):

        indicator = RealTimeIndicator('RVNUSDT', '5m')
        print(indicator.ema(5))
        print(indicator.rsi(14))
        print(indicator.bbands(20))
        print(indicator.candle())
