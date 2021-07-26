import csv
import time
from time import sleep

import numpy as np
from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import StrategyTest
from backtest.models import BackTest
from analytics.models import ExchangeRecord
import pandas as pd
import logging
from dateutil import parser
from binance import Client, BinanceSocketManager
from decouple import config
import btalib
import talib
import technic
from talib.abstract import *
from talib import abstract, SMA, EMA
import numpy
from numpy import genfromtxt
import backtrader as bt
import ccxt
import talib as ta

from datetime import datetime

logger = logging.getLogger('main')

client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


# https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):
        # file = 'backtest/file/daily.csv'
        #
        # csvfile = open(file, 'w', newline='')
        # candlestick_write = csv.writer(csvfile, delimiter=',')

        """
        [
          [
            1499040000000,      // Open time
            "0.01634790",       // Open
            "0.80000000",       // High
            "0.01575800",       // Low
            "0.01577100",       // Close
            "148976.11427815",  // Volume
            1499644799999,      // Close time
            "2434.19055334",    // Quote asset volume
            308,                // Number of trades
            "1756.87402397",    // Taker buy base asset volume
            "28.46694368",      // Taker buy quote asset volume
            "17928899.62484339" // Ignore.
          ]
        ]
        """
        klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1MINUTE, "26 Jul, 2018", "26 Jul, 2021")

        time = [entry[0] / 1000 for entry in klines]
        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]
        volume = [float(entry[5]) for entry in klines]

        close_array = np.asarray(close)
        ema9 = ta.EMA(close_array, timeperiod=9)
        ema50 = ta.EMA(close_array, timeperiod=50)
        ema100 = ta.RSI(close_array, timeperiod=100)
        # upperband, middleband, lowerband = ta.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

        diz = {}
        lenght = len(time)
        for i in range(lenght):
            diz = {
                'unix': time[i],
                'timestamp': datetime.fromtimestamp(time[i]),
                'open': open[i],
                'high': high[i],
                'low': low[i],
                'close': close[i],
                'volume': volume[i],
                'ema9': ema9[i],
                'ema50': ema50[i],
                'ema100': ema100[i]
            }
            print(diz)
        # for i in xrange(len(my_lis)):
        #     open_time = open_time[k]
        #     close = close[k]
        #     ema9 = ema9[k]
        #
        #     diz = {
        #         'open_time': open_time,
        #         'close': close,
        #         'ema9': ema9
        #     }
        # candlestick_processed = []
        # for data in candlesticks:
        #     candlestick = {
        #         "open": data[1],
        #         "high": data[2],
        #         "low": data[3],
        #         "close": data[4],
        #         'volume': data[5]
        #     }
        #     output = EMA(candlestick, timeperiod=25)
        #     print(output)
        #     candlestick_processed.append(candlestick)
