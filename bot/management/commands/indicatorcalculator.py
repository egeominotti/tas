from time import sleep

import decouple
import json
import redis
from django.core.management import BaseCommand
import logging
from backtest.services.computedata import compute_data_to_store
from bot.models import ComputedData
from bot.services.telegram import Telegram
from strategy.models import SymbolExchange, TimeFrame

logger = logging.getLogger('main')

r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)


class Command(BaseCommand):
    help = 'Indicator Calculator'

    def handle(self, *args, **kwargs):

        telegram = Telegram()
        symbols = SymbolExchange.objects.filter(market='FUTURES')
        time_frame = TimeFrame.objects.all()

        ComputedData.objects.all().delete()
        for interval in time_frame:
            for coin in symbols:
                key = str(coin.symbol) + "_" + str(interval) + "_" + coin.market
                if r.exists(key):
                    klines = json.loads(r.get(key))
                    if len(klines) > 0:
                        computed_data = compute_data_to_store(klines)
                        val = json.loads(computed_data)

                        if val.get('rsi') is not None:
                            rsi = round(val.get('rsi'), 3)
                            if rsi < 22:
                                message = 'Entry Possibile: ' + coin.symbol + \
                                          "\n" + 'Time Frame: ' + str(interval) + \
                                          "\n" + "RSI:" + str(rsi)
                                telegram.send(message)

                        ComputedData.objects.create(
                            key=key,
                            symbol=coin.symbol,
                            time_frame=interval,
                            data=computed_data
                        )
