from binance import Client
from binance.enums import *


class BinanceHelper:
    def __init__(self, api_key, api_secret, symbol, quantity, leverage):
        self.symbol = symbol
        self.quantity = quantity
        self.client = Client(api_key, api_secret)
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=leverage)

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
