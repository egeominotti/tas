from time import sleep

import numpy as np
import talib
from django.core.management import BaseCommand
import logging
import ccxt
from numpy import double

logger = logging.getLogger('main')
# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
index = 4  # use close price from each ohlcv candle

height = 15
length = 80


class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):

        '''
                    'options': {
                'defaultType': 'futures',
            },
        '''

        binance = ccxt.binance({
            'enableRateLimit': True,  # required https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
            'options': {
                'defaultType': 'future',
            },
        })
        symbol = 'RVN/USDT'
        timeframe = '5m'

        while True:
            try:
                ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=150)

                open = [double(entry[1]) for entry in ohlcv]
                high = [double(entry[2]) for entry in ohlcv]
                low = [double(entry[3]) for entry in ohlcv]
                close = [double(entry[4]) for entry in ohlcv]

                close_array = np.asarray(close)
                open_array = np.asarray(open)
                low_array = np.asarray(low)
                high_array = np.asarray(high)

                if len(close_array) >= 14 and close_array is not None:
                    rsi = talib.RSI(close_array, timeperiod=14)
                    print(round(rsi[-1], 4))

            except Exception as e:
                continue
