import json
import datetime
import sys
from time import sleep

import decouple
import redis
from django.http import JsonResponse
from bot.services.telegram import Telegram
from django.views.decorators.csrf import csrf_exempt
from binance import Client
from bot.models import UserExchange
from binance.enums import *
import requests

telegram = Telegram()
r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)


class ExchangeHelper:

    def __init__(
            self,
            client,
    ):
        self.client = client
        self.leverage = 1

    def get_leveraged_quantity(self, symbol):

        balance_wallet = self.get_current_balance_futures_() * 0.80
        quantity_precision_live = self.get_symbol_precision(symbol)
        price_coin = self.current_price_coin(symbol)

        total = (balance_wallet / price_coin) * self.leverage
        qty = round(total, quantity_precision_live)

        return qty

    def get_spot_quantity(self, symbol):

        balance_wallet = self.get_spot_quantity(symbol) * 0.80
        quantity_precision_live = self.get_symbol_precision(symbol)
        price_coin = self.current_price_coin(symbol)

        total = (balance_wallet / price_coin) * self.leverage
        qty = round(total, quantity_precision_live)

        return qty

    def get_symbol_precision(self, symbol):
        symbols_n_precision = {}
        info = self.client.futures_exchange_info()
        for item in info['symbols']:
            symbols_n_precision[item['symbol']] = item['quantityPrecision']

        return symbols_n_precision[symbol]

    def current_price_coin(self, symbol) -> float:

        resp = 0
        # if self.bot.market_spot:
        resp = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + symbol).json()
        # if self.bot.market_futures:
        # resp = requests.get('https://fapi.binance.com/fapi/v1/ticker/price?symbol=' + symbol).json()
        price = float(resp['price'])
        return price

    def get_current_balance_futures_(self, coin='USDT'):
        item = {}
        account_balance = self.client.futures_account_balance()

        for k in account_balance:
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
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=self.leverage)
        return self.client.futures_create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def buy_market_futures(self, quantity, symbol):
        # Change leverage
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=self.leverage)
        return self.client.futures_create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def sell_market_spot(self, quantity, symbol):
        return self.client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def buy_market_spot(self, quantity, symbol):
        return self.client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantity,
        )


def trading(id, user, ticker):
    """
    :param id:
    :param user:
    :param ticker:
    :return:
    """

    try:

        entry_text = ''
        key = user.user.username + "_" + ticker
        cl = Client(api_key=user.api_key, api_secret=user.api_secret)
        ex = ExchangeHelper(cl)

        # buy
        if id == 'EL':
            quantity = ex.get_spot_quantity(ticker)
            ex.buy_market_spot(quantity, ticker)

            balance = round(ex.get_spot_quantity(ticker), 3)
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            entry_text = "Entry Long: 📈 " + \
                         "\n" + "User: " + user.user.username + \
                         "\n" + "Balance: " + str(balance) + \
                         "\n" + "Ticker: " + str(ticker) + \
                         "\nDate: " + str(now)

            dictValue = {"quantity": float(quantity), "start_balance": float(balance)}
            r.set(key, json.dumps(dictValue))

        # sell
        if id == 'SL' or id == 'TP':

            value = json.loads(r.get(key))
            quantity = ex.get_spot_quantity(ticker)
            ex.sell_market_spot(quantity, ticker)

            balance = round(ex.get_spot_quantity(ticker) - value.get('start_balance'), 3)

            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            entry_text = "Exit Long: " + str(ticker) + " ✅ " + \
                         "\n" + "User: " + user.user.username + \
                         "\n" + "Profit or Loss: " + str(balance) + \
                         "\nDate: " + str(now)

        telegram.send(entry_text)
        sys.exit(1)

    except Exception as e:
        entry_text = "Error: " + str(e)
        telegram.send(entry_text)


@csrf_exempt
def webhook_tradingview(request):
    if request.method == 'POST':

        """
        id :
        ->
            EL -> Entry Long -> Buy order
            TP -> Take profit -> sell order
            SL -> Stop loss -> sell order
        """

        try:

            body = request.body.decode('utf-8')
            userexchange = UserExchange.objects.all()
            data = json.loads(body)

            id = data.get('id')
            ticker = data.get('ticker')

            for user in userexchange:
                trading(id, user, ticker)

        except Exception as e:

            entry_text = "Error: " + str(e)
            telegram.send(entry_text)

        return JsonResponse({})
