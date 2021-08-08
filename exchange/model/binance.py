import requests
from binance import Client
from binance.enums import *


class BinanceHelper:

    def __init__(
            self,
            api_key,
            api_secret,
            symbol,
            user,
            bot=None
    ):

        self.client = Client(api_key, api_secret)
        self.symbol = symbol
        self.user = user
        self.orderId = None

        if bot is not None:
            self.bot = bot
            self.leverage = self.bot.leverage

        if bot is not None:
            self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=self.bot.leverage)
        else:
            self.client.get_my_trades()
            self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=1)

    def get_quantity_from_number_of_bot(self):
        """
        :return: Entrata al 100% del capitale divisa per bot attivi per utente
        """
        # balance_wallet = (self.get_current_balance_futures_() - 0.5) / self.counter_bot
        balance_wallet = self.bot.amount - 0.5
        symbol_precision = self.get_symbol_precision()
        price_coin = self.current_price_coin()
        qty = round(balance_wallet / price_coin, symbol_precision)
        return qty

    def get_quantity(self):
        """
        :return: Entrata al 100% del capitale
        """
        # balance_wallet = self.get_current_balance_futures_() - 0.5
        balance_wallet = self.bot.amount - 0.5
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

    def get_current_investment_amount(self):
        return self.bot.amount

    def get_current_balance_futures_(self, coin='USDT'):
        item = {}
        for k in self.client.futures_account_balance():
            item[k['asset']] = k['balance']
        if coin is not None:
            return float(item[coin])
        return item

    def spot_balance(self):
        sum_btc = 0
        balances = self.client.get_account()
        for _balance in balances["balances"]:
            asset = _balance["asset"]
            if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
                try:
                    btc_quantity = float(_balance["free"]) + float(_balance["locked"])
                    if asset == "BTC":
                        sum_btc += btc_quantity
                    else:
                        _price = self.client.get_symbol_ticker(symbol=asset + "BTC")
                        sum_btc += btc_quantity * float(_price["price"])
                except:
                    pass

        current_btc_price_USD = self.client.get_symbol_ticker(symbol="BTCUSDT")["price"]
        own_usd = sum_btc * float(current_btc_price_USD)
        return own_usd

    def sell_market(self):
        self.orderId = self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=self.get_quantity(),
        )

    def buy_market(self):
        self.orderId = self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=self.get_quantity(),
        )

    def buy_limit(self):
        self.orderId = self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            quantity=self.get_quantity(),
        )

    def sell_limit(self, price):
        self.orderId = self.client.futures_create_order(
            symbol=self.symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            quantity=self.get_quantity(),
            price=price
        )

    def futures_cancel_order_(self):
        print(self.orderId)
        print(self.orderId)
        print(self.orderId)
        print(self.orderId)
        self.client.futures_cancel_order(symbol=self.orderId['symbol'], orderId=self.orderId['orderid'])
