import requests
import json
from binance import Client
from decouple import config
from binance.enums import *


class Binance:

    client = Client(config('api_key_binance'), config('api_secret_binance'))


    def __init__(self, symbol, quantity, leverage):
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=5)

    def buy(self):
         self.client.futures_create_order(
            symbol='BTCUSDT',
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=QUANTITY,
        )

    def sell(self):
        self.client.futures_create_order(
            symbol='BTCUSDT',
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=QUANTITY,
        )
