from binance import Client
from binance.enums import *
from decouple import config


class BinanceHelper:
    def __init__(self, symbol, quantity, leverage=1):
        self.symbol = symbol
        self.quantity = quantity
        # self.client = Client(api_key, api_secret)
        self.client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))

        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=leverage)

    def sell_market(self):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=self.quantity,
        )

    def buy_market(self):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=self.quantity,
        )

    def buy_limit(self):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            quantity=self.quantity,
        )

    def sell_limit(self, price):
        self.client.order_limit_sell(
            symbol=self.symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            quantity=self.quantity,
            price=price
        )
