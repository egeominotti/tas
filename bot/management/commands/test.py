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
        client = Client()


        # del close[0]
        # LEN = len(close)
        # close_array = np.asarray(close)
        # print(close_array)
        # if len(close_array) >= 14 and close_array is not None:
        #     rsi = talib.RSI(close_array, timeperiod=14)

        close_array = None
        arr2 = None
        while True:
            if close_array is None:
                klines = client \
                    .futures_klines(symbol='RVNUSDT',
                                    interval='1m',
                                    limit=250
                                    )
                del klines[-1]
                close = [double(entry[4]) for entry in klines]
                close_array = np.asarray(close)

                if len(close_array) >= 14 and close_array is not None:
                    rsi = talib.RSI(close_array, timeperiod=14)
                    print(rsi[-1])

            else:
                symbol = 'RVNUSDT'
                timeframe = '1m'
                key = symbol + "_" + str(timeframe) + "_FUTURES"
                data = json.loads(r.get(key))
                #close = [double(entry['candle_close']) for entry in data]
                if data.get('is_closed') is True:
                    arr2 = np.array([double(data['candle_close'])])
                    print(arr2)
                    print("iNSEISCO NUOVO VALORE")
                    r.set(key, json.dumps({'is_closed': False}))

            if arr2 is not None:
                arr_flat = np.append(close_array, arr2)
                print(arr_flat)

                if len(arr_flat) >= 14 and arr_flat is not None:
                    rsi = talib.RSI(arr_flat, timeperiod=14)
                    print(rsi[-1])

            sleep(1)
                #
                # arr_flat = np.append(close_array, arr2)
                # print(arr_flat)
                # if len(arr_flat) >= 14 and arr_flat is not None:
                #     rsi = talib.RSI(arr_flat, timeperiod=14)
                #     print(rsi[-1])
                # sleep(1)

