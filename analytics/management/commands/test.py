from exchange.model.binance import BinanceHelper
from django.core.management import BaseCommand
import logging

logger = logging.getLogger('main')


# twm = ThreadedWebsocketManager(api_key=config('API_KEY_BINANCE'), api_secret=config('API_SECRET_BINANCE'))


class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):
        bh = BinanceHelper(
            symbol='BTCUSDT',
        )
        print(bh.get_current_balance_futures_('USDT'))
