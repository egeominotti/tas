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

logger = logging.getLogger('main')

client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


def get_df(symbol):
    client_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume',
                      'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore']
    data = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "135 mins ago UTC")
    df = pd.DataFrame(data,
                      columns=['open_time', 'open', 'high', 'low', 'close', 'volume'],
                      dtype='float64')

    return df


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):
        # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

        #timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1m')
        print(get_df('BTCUSDT'))
        #print(timestamp)
        # bars = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=20000)
        # for line in bars:
        #     del line[5:]
        # #print(bars)
        # btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
        # btc_df.set_index('date', inplace=True)
        # btc_df.index = pd.to_datetime(btc_df.index, unit='ms')
        # btc_df['20sma'] = btc_df.close.rolling(20).mean()
        # sma = btalib.sma(btc_df.close)
        # print(sma.df)

