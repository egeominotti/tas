from datetime import datetime
from time import sleep
from analytics.services.exchangeApi import Taapi
from django.core.management import BaseCommand
import logging
from binance.enums import *
from binance import Client
from decouple import config

from dateutil import parser

logger = logging.getLogger('main')
lsitTimeSplit = [
    0, 15, 30, 45
]


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):

        TAKE_PROFIT = 1.02
        STOP_LOSS = 0.98
        RATIO = 1.00005
        QUANTITY = 0.004
        valueLong = 0

        long = False
        taapi = Taapi('BTC/USDT')
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))
        client.futures_change_leverage(symbol='BTCUSDT', marginType='ISOLATED', leverage=1)

        while True:

            now = datetime.now()
            candle_close = taapi.candle('1h').get('close')

            """
            Strategy Long with loss profit
            """
            if long is False:

                for k in lsitTimeSplit:

                    if k == now.minute:

                        ema1 = taapi.ema(9, '1h')
                        ema2 = taapi.ema(24, '1h')
                        ema3 = taapi.ema(100, '1h')

                        ratio_value = ema1 / ema2
                        if 1 < ratio_value < RATIO:
                            if candle_close > ema3:

                                print("---------------------------------------------------")
                                print("Compro LONG al prezzo: " + str(candle_close))
                                print("TP:" + str(candle_close * TAKE_PROFIT))
                                print("SL:" + str(candle_close * STOP_LOSS))
                                print("---------------------------------------------------")

                                client.futures_create_order(
                                    symbol='BTCUSDT',
                                    side=SIDE_BUY,
                                    type=ORDER_TYPE_MARKET,
                                    quantity=QUANTITY,
                                )

                                valueLong = candle_close
                                long = True

            if long is True:

                if candle_close > valueLong * TAKE_PROFIT:
                    print("Chiusura posizione long: " + str(valueLong * TAKE_PROFIT))

                    client.futures_create_order(
                        symbol='BTCUSDT',
                        side=SIDE_SELL,
                        type=ORDER_TYPE_MARKET,
                        quantity=QUANTITY,
                    )

                    long = False

                if candle_close < valueLong * STOP_LOSS:
                    print("STOP LOSS")

                    client.futures_create_order(
                        symbol='BTCUSDT',
                        side=SIDE_SELL,
                        type=ORDER_TYPE_MARKET,
                        quantity=QUANTITY,
                    )

                    long = False

            sleep(1)
