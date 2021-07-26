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

        # listema = [5, 7, 9, 10, 12, 24, 27,30, 42, 50, 60, 100, 200, 223, 365]
        # Timeframe 1m, 15m, 30m, 1h, 2h, 4h, 8h, 12h, 1D,3D,1

        klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, "17 Aug, 2017", "26 Jul, 2021")

        time = [entry[0] / 1000 for entry in klines]
        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]
        volume = [float(entry[5]) for entry in klines]

        close_array = np.asarray(close)
        ema5 = ta.EMA(close_array, timeperiod=5)
        ema7 = ta.EMA(close_array, timeperiod=7)
        ema9 = ta.EMA(close_array, timeperiod=9)
        ema10 = ta.EMA(close_array, timeperiod=10)
        ema12 = ta.EMA(close_array, timeperiod=12)
        ema24 = ta.EMA(close_array, timeperiod=24)
        ema27 = ta.EMA(close_array, timeperiod=27)
        ema30 = ta.EMA(close_array, timeperiod=30)
        ema42 = ta.EMA(close_array, timeperiod=42)
        ema50 = ta.EMA(close_array, timeperiod=50)
        ema60 = ta.EMA(close_array, timeperiod=60)
        ema100 = ta.EMA(close_array, timeperiod=100)
        ema200 = ta.EMA(close_array, timeperiod=200)
        ema223 = ta.EMA(close_array, timeperiod=223)
        ema365 = ta.EMA(close_array, timeperiod=365)


        diz = {}
        lenght = len(time)
        for i in range(lenght):

            diz[time[i]] = {
                'unix': time[i],
                'timestamp': datetime.fromtimestamp(time[i]),
                'open': open[i],
                'high': high[i],
                'low': low[i],
                'close': close[i],
                'volume': volume[i],
                'ema5': ema5[i],
                'ema7': ema7[i],
                'ema9': ema9[i],
                'ema10': ema10[i],
                'ema12': ema12[i],
                'ema24': ema24[i],
                'ema27': ema27[i],
                'ema30': ema30[i],
                'ema42': ema42[i],
                'ema50': ema50[i],
                'ema60': ema60[i],
                'ema100': ema100[i],
                'ema200': ema200[i],
                'ema223': ema223[i],
                'ema365': ema365[i]
            }
        print(diz)
