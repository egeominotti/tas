from time import sleep
import datetime
import decouple
import json

import numpy as np
import redis
import talib
from django.core.management import BaseCommand
import logging

from numpy import double

from backtest.services.computedata import compute_data_to_store
from bot.models import ComputedData
from bot.services.telegram import Telegram
from strategy.models import SymbolExchange, TimeFrame

logger = logging.getLogger('main')

redis = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)


class Indicators:

    def __init__(self, symbol, time_frame, redis):
        self.symbol = symbol
        self.time_frame = time_frame
        self.redis_client = redis
        self.close_array = None
        self.open_array = None
        self.low_array = None
        self.high_array = None
        self.key = str(self.symbol) + "_" + str(self.time_frame) + "_FUTURES"
        if self.redis_client.exists(self.key):
            klines = json.loads(self.redis_client.get(self.key))

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

    def candle(self, backtrack=-1):
        if self.redis_client.exists(self.key):
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

        return 0

    def ema(self, period, backtrack=-1):
        if self.redis_client.exists(self.key):
            if len(self.close_array) >= period and self.close_array is not None:
                ema = talib.EMA(self.close_array, timeperiod=period)
                return round(ema[backtrack], 5)

        return 0

    def rsi(self, period, backtrack=-1):
        if self.redis_client.exists(self.key):

            if len(self.close_array) >= period and self.close_array is not None:
                rsi = talib.RSI(self.close_array, timeperiod=period)
                return round(rsi[backtrack], 4)

        return 0

    def bbands(self, period=20, backtrack=-1):
        if self.redis_client.exists(self.key):
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


class Command(BaseCommand):
    help = 'Indicator Calculator'

    def handle(self, *args, **kwargs):

        telegram = Telegram()
        symbols = SymbolExchange.objects.filter(market='FUTURES')
        # time_frame = TimeFrame.objects.all()

        ComputedData.objects.all().delete()
        for coin in symbols:

            indicators1h = Indicators(
                coin.symbol,
                '1h',
                redis
            )

            indicators4h = Indicators(
                coin.symbol,
                '4h',
                redis
            )

            indicators1d = Indicators(
                coin.symbol,
                '1d',
                redis
            )

            if indicators1d.ema(26) > indicators1d.ema(200):
                    if 46 < indicators1d.rsi(14) < 54:
                        if indicators4h.rsi(14) < 37.5 and indicators1h.rsi(14) < 31:
                            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            message = '‼️+ Entry Short: ' + coin.symbol + " " \
                                                                          "\n" + 'Candle close: ' + str(
                                indicators1d.candle().get('close')) + \
                                      "\n" + "Date: " + str(now)
                            telegram.send(message)

            if indicators1d.ema(26) < indicators1d.ema(200):
                    if 46 < indicators1d.rsi(14) < 54:
                        if indicators4h.rsi(14) > 65 and indicators1h.rsi(14) > 70:
                            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            message = '‼️+ Entry Short: ' + coin.symbol + " " \
                                                                          "\n" + 'Candle close: ' + str(
                                indicators1d.candle().get('close')) + \
                                      "\n" + "Date: " + str(now)
                            telegram.send(message)

            # ComputedData.objects.create(
            #     key=key,
            #     symbol=coin.symbol,
            #     time_frame=interval,
            #     data=computed_data
            # )
