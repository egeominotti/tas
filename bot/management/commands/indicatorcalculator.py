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
    LIMIT_KLINE = 200
    close_array = None
    open_array = None
    low_array = None
    high_array = None

    def __init__(self, symbol, time_frame, redis):
        self.symbol = symbol
        self.time_frame = time_frame
        self.redis_client = redis

    def compute(self, real_time):

        self.close_array = None
        self.open_array = None
        self.low_array = None
        self.high_array = None

        key = str(self.symbol) + "_" + str(self.time_frame) + "_FUTURES"
        key2 = str(self.symbol) + "_" + str(self.time_frame) + "_FUTURES" + "_CANDLE"

        try:

            klines = json.loads(self.redis_client.get(key))
            klines_realtime = json.loads(self.redis_client.get(key2))

            if klines is not None and klines_realtime is not None:

                if len(klines) > 0 and len(klines_realtime) > 0:

                    if real_time is False:
                        open = [double(entry[1]) for entry in klines]
                        high = [double(entry[2]) for entry in klines]
                        low = [double(entry[3]) for entry in klines]
                        close = [double(entry[4]) for entry in klines]

                        self.close_array = np.asarray(close)
                        self.open_array = np.asarray(open)
                        self.low_array = np.asarray(low)
                        self.high_array = np.asarray(high)

                    if real_time is True:
                        open = [double(entry[1]) for entry in klines]
                        high = [double(entry[2]) for entry in klines]
                        low = [double(entry[3]) for entry in klines]
                        close = [double(entry[4]) for entry in klines]

                        self.close_array = np.asarray(close)
                        self.open_array = np.asarray(open)
                        self.low_array = np.asarray(low)
                        self.high_array = np.asarray(high)

                        self.close_array = np.append(self.close_array, [klines_realtime.get('close')])
                        self.open_array = np.append(self.open_array, [klines_realtime.get('open')])
                        self.low_array = np.append(self.low_array, [klines_realtime.get('low')])
                        self.high_array = np.append(self.high_array, [klines_realtime.get('high')])

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

    def supertrend(self, period, multiplier=3):

        atr = talib.ATR(self.high_array, self.low_array, self.close_array, period=period)
        basic_upperband = (self.high_array + self.low_array / 2) + (multiplier + atr)
        basic_lowerband = (self.high_array + self.low_array / 2) - (multiplier + atr)

        print(basic_lowerband)

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
            indicators1h.compute(False)

            indicators4h = Indicators(
                coin.symbol,
                '4h',
                redis
            )
            indicators4h.compute(False)

            indicators1d = Indicators(
                coin.symbol,
                '1d',
                redis
            )
            indicators1d.compute(False)
            indicators1d.rsi(14)

            if indicators1d.ema(26) > indicators1d.ema(200):
                if indicators1d.candle().get('close') > indicators1d.ema(26):
                    if 46 < indicators1d.rsi(14) < 54:
                        if indicators4h.rsi(14) < 37.5 and indicators1d.rsi(14) < 31:

                            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            message = '‼️+ Entry Short: ' + coin.symbol + " " \
                                      "\n" + 'Candle close: ' + str(indicators1d.candle().get('close')) + \
                                      "\n" + "Date: " + str(now)
                            telegram.send(message)

                # computed_data = compute_data_to_store(klines)
                # val = json.loads(computed_data)
                #
                # if val.get('rsi') is not None:
                #
                #     rsi = round(val.get('rsi'), coin.quantity_precision)
                #     close = round(val.get('close'), coin.quantity_precision)
                #     ema200 = round(val.get('ema200'), coin.quantity_precision)
                #     ema223 = round(val.get('ema223'), coin.quantity_precision)
                #     ema60 = round(val.get('ema60'), coin.quantity_precision)
                #     ema50 = round(val.get('ema50'), coin.quantity_precision)
                #     ema5 = round(val.get('ema5'), coin.quantity_precision)
                #     ema10 = round(val.get('ema10'), coin.quantity_precision)
                #     upperband = round(val.get('upperband'), coin.quantity_precision)
                #     middleband = round(val.get('middleband'), coin.quantity_precision)
                #     lowerband = round(val.get('lowerband'), coin.quantity_precision)
                #
                #     # Short signal
                #     if ema60 == ema223:
                #         now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                #         message = '‼️+ Entry Short: ' + coin.symbol + " " \
                #                                                       "\n" + 'Candle close: ' + str(close) + \
                #                   "\n" + 'Time Frame: ' + str(interval) + \
                #                   "\n" + 'Ema 60 == ema 223: ' + str(interval) + \
                #                   "\n" + "Candle Close: " + str(close) + \
                #                   "\n" + "RSI: " + str(rsi) + \
                #                   "\n" + "Upperband: " + str(upperband) + \
                #                   "\n" + "Middleband: " + str(middleband) + \
                #                   "\n" + "Lowerband: " + str(lowerband) + \
                #                   "\n" + "ema223: " + str(ema223) + \
                #                   "\n" + "ema60: " + str(ema60) + \
                #                   "\n" + "Date: " + str(now)
                #         telegram.send(message)
                #
                #     # Long signal
                #     if ema200 < close:
                #         if rsi < 30 and close <= lowerband:
                #             now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                #             message = '‼️+ Entry Long: ' + coin.symbol + " " \
                #                                                          "\n" + 'Candle close: ' + str(close) + \
                #                       "\n" + 'Time Frame: ' + str(interval) + \
                #                       "\n" + "Candle Close: " + str(close) + \
                #                       "\n" + "RSI: " + str(rsi) + \
                #                       "\n" + "Upperband: " + str(upperband) + \
                #                       "\n" + "Middleband: " + str(middleband) + \
                #                       "\n" + "Lowerband: " + str(lowerband) + \
                #                       "\n" + "ema200: " + str(ema200) + \
                #                       "\n" + "Date: " + str(now)
                #             telegram.send(message)
                #
                #     # Short signal
                #     if ema200 > close:
                #         if rsi > 70 and close >= upperband:
                #             now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                #             message = '‼️+ Entry Short: ' + coin.symbol + " " \
                #                                                           "\n" + 'Candle close: ' + str(close) + \
                #                       "\n" + 'Time Frame: ' + str(interval) + \
                #                       "\n" + "Candle Close: " + str(close) + \
                #                       "\n" + "RSI: " + str(rsi) + \
                #                       "\n" + "Upperband: " + str(upperband) + \
                #                       "\n" + "Middleband: " + str(middleband) + \
                #                       "\n" + "Lowerband: " + str(lowerband) + \
                #                       "\n" + "ema200: " + str(ema200) + \
                #                       "\n" + "Date: " + str(now)
                #             telegram.send(message)
                #
                # ComputedData.objects.create(
                #     key=key,
                #     symbol=coin.symbol,
                #     time_frame=interval,
                #     data=computed_data
                # )
