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
from talib import abstract, SMA
import numpy
from numpy import genfromtxt
import backtrader as bt
import ccxt

from datetime import datetime

logger = logging.getLogger('main')

client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


# https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):

        file = 'backtest/file/daily.csv'

        csvfile = open(file, 'w', newline='')
        candlestick_write = csv.writer(csvfile, delimiter=',')
        candlesticks = client.get_historical_klines('BTCUSDT', '1h', "1 Jan, 2021", "30 Jan, 2021")


        candlestick_processed = []
        for data in candlesticks:
            candlestick = {
                "time": data[0],
                "open": data[1],
                "high": data[2],
                "low": data[3],
                "close": data[4]
            }
            candlestick_processed.append(candlestick)

        for candlestick in candlesticks:
            candlestick[0] = candlestick[0] / 100
            candlestick_write.writerow(candlestick)

        my_data = genfromtxt(file, delimiter='')
        close = my_data[:, 4]
        print(close)

        ema9 = talib.EMA(close, timeperiod=9)
        ema24 = talib.EMA(close, timeperiod=24)
        ema50 = talib.EMA(close, timeperiod=50)
