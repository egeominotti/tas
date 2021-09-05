from strategy.models import SymbolExchange
from django.core.management import BaseCommand
import logging
import ccxt

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Download Info coins'

    def handle(self, *args, **kwargs):

        SymbolExchange.objects.all().delete()

        #exchanges = ['coinbasepro', 'kraken', 'binanceusdm', 'binance']
        exchanges = ['binanceusdm', 'binance']

        for exchange in exchanges:

            exchange_id = exchange
            exchange_class = getattr(ccxt, exchange_id)
            exchange_instance = exchange_class({})
            markets = exchange_instance.load_markets()

            for k in markets:

                type_of_market = ''
                if exchange == 'binance':
                    type_of_market = 'SPOT'
                if exchange == 'binanceusdm':
                    type_of_market = 'FUTURES'

                if markets[k]['quote'] == 'USDT' and markets[k]['info']['status'] == 'TRADING' and markets[k]['active']:
                    # if markets[k]['quote'] == 'USDT' and markets[k]['info']['status'] == 'TRADING' and markets[k]['active']:
                    # print(markets[k]['precision'])

                    symbol = markets[k]['id']
                    quantity_precision = markets[k]['precision']['price']
                    precision = markets[k]['precision']['amount']

                    SymbolExchange.objects.create(
                        symbol=symbol,
                        precision=precision,
                        quantity_precision=quantity_precision,
                        market=type_of_market,
                        exchange=exchange
                    )
