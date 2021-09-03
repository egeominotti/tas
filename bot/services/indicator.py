import json
import talib
import numpy as np
from time import sleep
from binance import Client
from numpy import double


class Indicators:
    LIMIT_KLINE = 200
    close_array = None
    open_array = None
    low_array = None
    high_array = None

    def __init__(self, bot, symbol, time_frame, redis):
        self.bot = bot
        self.symbol = symbol
        self.time_frame = time_frame
        self.redis = True
        self.redis_client = redis

    def compute(self, real_time):

        klines = None

        self.close_array = None
        self.open_array = None
        self.low_array = None
        self.high_array = None

        self.key = None
        if self.bot.market_spot:
            self.key = str(self.symbol) + "_" + str(self.time_frame) + "_SPOT"
        if self.bot.market_futures:
            self.key = str(self.symbol) + "_" + str(self.time_frame) + "_FUTURES"

        try:

            if real_time is False:
                klines = json.loads(self.redis_client.get(self.key))

            if real_time is True:

                client = Client()
                if self.bot.market_futures:
                    klines = client.futures_klines(
                        symbol=self.symbol,
                        interval=self.time_frame,
                        limit=self.LIMIT_KLINE
                    )

                if self.bot.market_spot:
                    klines = client.get_klines(
                        symbol=self.symbol,
                        interval=self.time_frame,
                        limit=self.LIMIT_KLINE,
                    )

            if klines is not None:

                if len(klines) > 0:
                    open = [double(entry[1]) for entry in klines]
                    high = [double(entry[2]) for entry in klines]
                    low = [double(entry[3]) for entry in klines]
                    close = [double(entry[4]) for entry in klines]

                    self.close_array = np.asarray(close)
                    self.open_array = np.asarray(open)
                    self.low_array = np.asarray(low)
                    self.high_array = np.asarray(high)

        except Exception as e:
            # retry connection
            print("Compute Error:" + str(e))
            sleep(30)

    def candle(self, backtrack=-1):

        if self.open_array is not None and \
                self.high_array is not None and \
                self.low_array is not None and \
                self.close_array is not None:

            if len(self.open_array) > 0 and \
                    len(self.high_array) > 0 and \
                    len(self.low_array) > 0 and \
                    len(self.close_array):
                value = {
                    'open': self.open_array[backtrack],
                    'high': self.high_array[backtrack],
                    'low': self.low_array[backtrack],
                    'close': self.close_array[backtrack],
                }
                return value

        value = {
            'open': 0,
            'high': 0,
            'low': 0,
            'close': 0,
        }
        return value

    def ema(self, period, backtrack=-1):

        if len(self.close_array) >= period and self.close_array is not None:
            ema = talib.EMA(self.close_array, timeperiod=period)
            return round(ema[backtrack], 5)

        return 0

    def rsi(self, period, backtrack=-1):

        if len(self.close_array) >= period and self.close_array is not None:
            rsi = talib.RSI(self.close_array, timeperiod=period)
            return round(rsi[backtrack], 4)

        return 0

    def bbands(self, period=20, backtrack=-1):

        if len(self.close_array) >= period and self.close_array is not None:
            upperband, middleband, lowerband = talib.BBANDS(
                self.close_array,
                timeperiod=period,
                nbdevup=2,
                nbdevdn=2,
                matype=0)

            bbands = {
                'valueUpperBand': round(upperband[backtrack], 5),
                'valueMiddleBand': round(middleband[backtrack], 5),
                'valueLowerBand': round(lowerband[backtrack], 5)
            }

            return bbands

        return 0
