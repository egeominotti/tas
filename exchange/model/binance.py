import requests
from binance import Client
from binance.enums import *
from bot.models import Bot
from exchange.models import User

class BinanceHelper:
    def __init__(self, api_key, api_secret, symbol, user, leverage=1):
        self.symbol = symbol
        self.user = user
        self.leverage = leverage
        self.client = Client(api_key, api_secret)
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=leverage)

    def get_quantity_from_number_of_bot(self):
        """
        :return: Entrata al 100% del capitale divisa per bot attivi per utente
        """
        balance_wallet = (self.get_current_balance_futures_() - 0.5) / self.user.counter_bot
        symbol_precision = self.get_symbol_precision()
        price_coin = self.current_price_coin()
        qty = round(balance_wallet / price_coin, symbol_precision)
        return qty

    def get_quantity(self):
        """
        :return: Entrata al 100% del capitale
        """
        balance_wallet = self.get_current_balance_futures_() - 0.5
        symbol_precision = self.get_symbol_precision()
        price_coin = self.current_price_coin()
        qty = round(balance_wallet / price_coin, symbol_precision)
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
