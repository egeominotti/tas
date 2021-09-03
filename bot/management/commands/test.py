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
        client = Client('vyghMLzH2Pvr0TCoV11Equ9kIK2jxL6ZpDh8pyUBz4hvAWXSLWO6rBHbogQmX9lH',
                        'yTmr8uu0w3ARIzTlYadGkWX79BlTHSybzzJeInrWcjUoygP3K7t81j4WXd8amMOM')

        client.futures_change_leverage(symbol='ETHUSDT', marginType='ISOLATED', leverage=2)
        order = client.futures_create_order(
            symbol='ETHUSDT',
            side='SELL',
            type='MARKET',
            quantity=0.02,
        )
        val = client.futures_get_order(symbol=order.get('symbol'), orderId=order.get('orderId'))
        print(val.get('avgPrice'))
        # info_spot = client.get_exchange_info()
        # info_futures = client.futures_exchange_info()
        #
        # coinsspot = []
        # for coins_futures in info_spot['symbols']:
        #     coinsspot.append(coins_futures['symbol'])
        # print(len(coinsspot))
        #
        # coinsfutures = []
        # for coins_futures in info_futures['symbols']:
        #     print(coins_futures['pricePrecision'])
        #     coinsfutures.append(coins_futures['symbol'])
        # print(len(coinsfutures))
