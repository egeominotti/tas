from time import sleep

import decouple
import json
import numpy as np
import redis
import talib
from binance import Client
from django.core.management import BaseCommand
import logging
import ccxt
from numpy import double

logger = logging.getLogger('main')
redis = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)
KEY = 'FUTURES'

class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):

        symbol = 'RVNUSDT'
        timeframe = '5m'

        key = symbol + "_" + timeframe + "_" + KEY
        key2 = symbol + "_" + timeframe + "_" + KEY + "_CANDLE"

        while True:
            klines = json.loads(redis.get(key))
            klines_realtime =  json.loads(redis.get(key2))
            close = [double(entry[4]) for entry in klines]
            close_array = np.asarray(close)
            arr_flat = np.append(close_array, [klines_realtime.get('close')])
            rsi = talib.RSI(arr_flat, timeperiod=14)
            print(round(rsi[-1], 4))
