from time import sleep
import requests
from binance import Client
from binance.enums import *


class BinanceHelper:
    def __init__(self, api_key, api_secret, symbol, leverage=1):
        self.symbol = symbol
        self.leverage = leverage
        self.client = Client(api_key, api_secret)
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=leverage)

    def get_quantity(self):

        current_balance =  self.get_current_balance_futures_() - 0.5
        symbol_precision = self.get_symbol_precision()
        price_coin=        self.current_price_coin()

        qty = round(self.get_current_balance_futures_() - 0.5 / self.current_price_coin(), 1)
        return qty

    def get_symbol_precision(self):
        symbols_n_precision = {}
        info = self.client.futures_exchange_info()
        for item in info['symbols']:
            symbols_n_precision[item['symbol']] = item['quantityPrecision']
        return symbols_n_precision[self.symbol]

    def current_price_coin(self) -> float:
        resp = requests.get('https://api.binance.com/api/v1/ticker/price?symbol=' + self.symbol).json()
        price = float(resp['price'])
        return price

    def get_current_balance_futures_(self, coin='USDT'):
        item = {}
        for k in self.client.futures_account_balance():
            item[k['asset']] = k['balance']
        if coin is not None:
            return float(item[coin])
        return item

    def sell_market(self):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=self.get_quantity(),
        )

    def buy_market(self):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=self.get_quantity(),
        )

    def buy_limit(self):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            quantity=self.get_quantity(),
        )

    def sell_limit(self, price):
        self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            quantity=self.get_quantity(),
            price=price
        )
