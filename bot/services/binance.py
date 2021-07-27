from binance import Client
from binance.enums import *
from decouple import config


class BinanceHelper:
    def __init__(self, symbol, quantity, leverage=1):
        self.client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=leverage)
        self.quantity = quantity
        self.symbol = symbol

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
