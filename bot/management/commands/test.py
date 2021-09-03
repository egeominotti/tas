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
# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
index = 4  # use close price from each ohlcv candle

r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)
KEY = 'FUTURES'

class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):

        symbol = 'RVNUSDT'
        timeframe = '5m'
        key = symbol + "_" + timeframe + "_" + KEY + "_" + "_REALTIME"
        while True:
            data = r.smembers(key)
            for k in data:
                print(k[0])
        # print(data)
        # close = [double(entry[4]) for entry in data]
        # close_array = np.asarray(close)
        # if len(close_array) > 14 and close_array is not None:
        #     rsi = talib.RSI(close_array, timeperiod=14)
        #     print(rsi[-1])
