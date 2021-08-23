import decouple
import json
import redis
from django.core.management import BaseCommand
import logging
from bot.services.indicator import RealTimeIndicator
from strategy.models import SymbolExchange

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Valori real time delle candele'

    def handle(self, *args, **kwargs):
        r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)

        times = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

        symbolList = []
        for symbol in SymbolExchange.objects.all():
            symbolList.append(symbol.symbol.lower())

        for symbol in symbolList:
            for interval in times:
                key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval) + "_CLOSED"
                if r.exists(key):
                    val = r.get(key)
                    print(val)
                    print(val)
                    for k in val:
                        print(k['candle_close'])


        # indicator = RealTimeIndicator('RVNUSDT', '1m','vyghMLzH2Pvr0TCoV11Equ9kIK2jxL6ZpDh8pyUBz4hvAWXSLWO6rBHbogQmX9lH','yTmr8uu0w3ARIzTlYadGkWX79BlTHSybzzJeInrWcjUoygP3K7t81j4WXd8amMOM')
        # indicator.compute()
        # print(indicator.ema(5))
        # print(indicator.rsi(14))
        # print(indicator.bbands(20))
        # print(indicator.candle())
