from binance import Client
from binance.enums import *
from decouple import config


class BinanceHelper:
    def __init__(self, symbol, quantity, leverage=1):
        self.symbol = symbol
        self.quantity = quantity
        # self.client = Client(api_key, api_secret)
        self.client = client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))
        self.client = client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=leverage)

    def sell(self):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=self.quantity,
        )

    def buy(self):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=self.quantity,
        )
