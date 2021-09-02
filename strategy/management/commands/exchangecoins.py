from strategy.models import SymbolExchange
from binance import Client
from django.core.management import BaseCommand
import logging
import ccxt
logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Download Info coins'

    def handle(self, *args, **kwargs):

        SymbolExchange.objects.all().delete()

        client = Client()
        info_spot = client.get_exchange_info()
        info_futures = client.futures_exchange_info()

        for coins_spot in info_spot['symbols']:
            status = coins_spot['status']
            if status == 'TRADING':
                symbol = coins_spot['symbol']
                #precision = coins_spot['pricePrecision']
                #quantity_precision = coins_spot['quantityPrecision']
                SymbolExchange.objects.create(
                    symbol=symbol,
                    market='SPOT',
                    #precision=precision,
                    #quantity_precision = quantity_precision,
                    exchange='BINANCE'
                )

        for coins_futures in info_futures['symbols']:
            status = coins_futures['status']
            if status == 'TRADING':
                symbol = coins_futures['symbol']
                precision = coins_futures['pricePrecision']
                quantity_precision = coins_futures['quantityPrecision']
                SymbolExchange.objects.create(
                    symbol=symbol,
                    market='FUTURES',
                    precision=precision,
                    quantity_precision = quantity_precision,
                    exchange='BINANCE'
                )