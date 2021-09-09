import json
from django.http import JsonResponse
from bot.services.telegram import Telegram
from django.views.decorators.csrf import csrf_exempt
from binance import Client
from bot.models import Bot, UserExchange
import requests

telegram = Telegram()

class ExchangeHelper:

    def __init__(
            self,
            client,
            leverage
    ):
        self.client = client
        self.leverage = leverage

    def get_leveraged_quantity(self, symbol):

        balance_wallet = self.get_current_balance_futures_() * 0.50
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
        #if self.bot.market_spot:
        #    resp = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + symbol).json()
        #if self.bot.market_futures:
        resp = requests.get('https://fapi.binance.com/fapi/v1/ticker/price?symbol=' + symbol).json()
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

    def get_order_entry_price(self, symbol, orderId):
        return float(self.client.futures_get_order(symbol=symbol, orderId=orderId).get('avgPrice'))


leverage = 10

@csrf_exempt
def webhook_tradingview(request):

    if request.method == 'POST':

        data = json.loads(request.body)


        exchange = data.get('exchange')
        ticker = data.get('ticker')
        time = data.get('time')

        market = ''
        if 'PERP' in ticker:
            market = 'FUTURES'
        else:
            market = 'SPOT'

        for user in UserExchange.objects.all():
            print(user)
            print(user.api_secret)
            cl = Client(api_key=user.api_key, api_secret=user.api_secret)
            ex = ExchangeHelper(cl, leverage)


        text = "Hi, from TradingView signal: " + exchange + " " + ticker + " " + str(time)
        telegram.send(text)

        return JsonResponse({})
