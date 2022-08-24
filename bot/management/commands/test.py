from time import sleep
import ccxt

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
redis = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)
KEY = 'FUTURES'


def get_current_balance_futures_(self, coin='USDT'):
    item = {}
    for k in self.client.futures_account_balance():
        item[k['asset']] = k['balance']
    if coin is not None:
        return float(item[coin])
    return item

class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):

        exchange_id = 'binance'
        exchange_class = getattr(ccxt, exchange_id)

        exchange = exchange_class({
            'apiKey': '',
            'secret': '',
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',  # ←-------------- quotes and 'future'
            },
        })

        #print(exchange.id, exchange.load_markets())
        print(exchange.fetch_balance())

        coin = 'USDT'
        item = {}
        for k in exchange.fetch_balance():
            item[k['asset']] = k['balance']
            print(item)
        # hitbtc = ccxt.hitbtc({'verbose': True})
        # hitbtc.fetch_balance()
        # hitbtc.create_market_buy_order()
        # hitbtc.create_market_sell_order()
