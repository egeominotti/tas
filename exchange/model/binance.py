import requests
from binance.enums import *
from binance.enums import SIDE_BUY


class BinanceHelper:

    def __init__(
            self,
            client,
            user,
            bot
    ):
        self.client = client
        self.user = user
        self.bot = bot
        self.leverage = self.bot.leverage

    def get_cluster_quantity(self, symbol):
        """
        :return: Entrata al 100% del capitale
        """
        balance_wallet = self.get_current_balance_futures_() - 0.5
        symbol_precision = self.get_symbol_precision(symbol)
        price_coin = self.current_price_coin(symbol)
        qty = round(balance_wallet / price_coin, symbol_precision)

        return qty

    def get_symbol_precision(self, symbol):
        symbols_n_precision = {}
        info = self.client.futures_exchange_info()
        for item in info['symbols']:
            symbols_n_precision[item['symbol']] = item['quantityPrecision']

        return symbols_n_precision[symbol]

    def current_price_coin(self, symbol) -> float:
        resp = requests.get('https://api.binance.com/api/v1/ticker/price?symbol=' + symbol).json()
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

    def sell_market_futures(self, quantity, symbol):
        # Change leverage
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=self.bot.leverage)
        self.client.futures_create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def buy_market_futures(self, quantity, symbol):
        # Change leverage
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=self.bot.leverage)
        self.client.futures_create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def sell_market_spot(self, quantity, symbol):
        self.client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def buy_market_spot(self, quantity, symbol):
        self.client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def buy_limit(self, quantity, symbol):
        self.client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def takeprofit_limit_long(self, quantity, symbol, price):
        self.client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
            quantity=quantity,
            price=price
        )

    def takeprofit_limit_short(self, quantity, symbol, price):
        self.client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
            quantity=quantity,
            price=price
        )

    def stoploss_limit_short(self, quantity, symbol, price):
        self.client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_STOP_LOSS_LIMIT,
            quantity=quantity,
            price=price
        )

    def stoploss_limit_long(self, quantity, symbol, price):
        self.client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_STOP_LOSS_LIMIT,
            quantity=quantity,
            price=price
        )

    def get_order(self, symbol, orderId):
        # return self.client.get_order(symbol=symbol, orderId=orderId)
        return self.client.get_order(symbol=symbol, orderId=orderId)

    def futures_cancel_order_(self):
        pass
