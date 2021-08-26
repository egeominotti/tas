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

height = 15
length = 80
r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)


class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):
        LEN = 0
        client = Client()

        symbol = 'RVNUSDT'
        timeframe = '1m'
        key = symbol + "_" + str(timeframe) + "_FUTURES"
        klines = json.loads(r.get(key))
        close = [double(entry['candle_close']) for entry in klines]
        del close[0]
        LEN = len(close)
        close_array = np.asarray(close)
        print(close_array)
        if len(close_array) >= 14 and close_array is not None:
            rsi = talib.RSI(close_array, timeperiod=14)

        klines = client \
            .futures_klines(symbol='RVNUSDT',
                            interval='1m',
                            limit=150
                            )
        del klines[-1]
        close = [double(entry[4]) for entry in klines]
        close_array = np.asarray(close)
        print(close_array)
        if len(close_array) >= 14 and close_array is not None:
            rsi = talib.RSI(close_array, timeperiod=14)
            print(rsi[-1])
        print(len(klines))
