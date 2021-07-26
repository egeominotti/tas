import csv
from time import sleep

from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import StrategyTest
from backtest.models import BackTest
from analytics.models import ExchangeRecord
import pandas as pd
import logging
from dateutil import parser
from binance import Client
from decouple import config
import btalib
import talib
import technic
from talib.abstract import *
from talib import abstract, SMA
import numpy
from numpy import genfromtxt
import backtrader as bt

logger = logging.getLogger('main')

client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


# https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
def get_df(symbol):
    client_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume',
                      'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore']
    data = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "135 mins ago UTC")
    df = pd.DataFrame(data,
                      columns=['open_time', 'open', 'high', 'low', 'close', 'volume'],
                      dtype='float64')

    return df


class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)

    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)
        if self.rsi < 70 and not self.position:
            self.buy(size=1)


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):
        file = 'backtest/file/daily.csv'

        csvfile = open(file, 'w', newline='')
        candlestick_write = csv.writer(csvfile, delimiter=',')
        candlesticks = client.get_historical_klines('BTCUSDT', '1h', "1 Jan, 2019", "1 Jan, 2021")

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

        ema9 = talib.EMA(close, timeperiod=9)
        ema24 = talib.EMA(close, timeperiod=24)
        ema50 = talib.EMA(close, timeperiod=50)
        print(ema9)
        print(ema24)
        print(ema50)
