from binance.enums import *
from binance import Client
from decouple import config
from time import sleep
from analytics.services.exchangeApi import Taapi
from django.core.management import BaseCommand
import telegram
import requests

import logging
from django.conf import settings

logger = logging.getLogger('main')


def telegram_bot_sendtext(bot_message):
    bot_token = '1889367095:AAGS13rjA6xWAGvcUTOy1W1vUZvPnNxcDaw'
    bot_chatID = '655989560'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


class Command(BaseCommand):
    help = 'Bot-Scalping-Ema-9-24-100'

    def handle(self, *args, **kwargs):

        telegram_bot_sendtext("START BOT Bot-Scalping-Ema-9-24-100")
        TAKE_PROFIT = 1.02
        STOP_LOSS = 0.98
        RATIO = 1.00005
        QUANTITY = 0.004
        valueLong = 0

        time_frame = '15m'

        LIVE = False

        long = False
        taapi = Taapi('BTC/USDT')
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))
        client.futures_change_leverage(symbol='BTCUSDT', marginType='ISOLATED', leverage=1)

        while True:

            candle_close = taapi.candle(time_frame).get('close')

            if long is False:

                ema1 = taapi.ema(9, time_frame)
                ema2 = taapi.ema(24, time_frame)
                ema3 = taapi.ema(100, time_frame)

                ratio_value = ema1 / ema2
                telegram_bot_sendtext("RATIO VALUE: " + str(ratio_value))
                if 1 < ratio_value < RATIO:
                    if candle_close > ema3:

                        s1 = "Compro LONG al prezzo: " + str(candle_close)
                        s2 = "TP:" + str(candle_close * TAKE_PROFIT)
                        s3 = "SL:" + str(candle_close * STOP_LOSS)

                        telegram_bot_sendtext(s1)
                        telegram_bot_sendtext(s2)
                        telegram_bot_sendtext(s3)

                        print("---------------------------------------------------")
                        print(s1)
                        print(s2)
                        print(s3)
                        print("---------------------------------------------------")

                        if LIVE:
                            client.futures_create_order(
                                symbol='BTCUSDT',
                                side=SIDE_BUY,
                                type=ORDER_TYPE_MARKET,
                                quantity=QUANTITY,
                            )

                        valueLong = candle_close
                        long = True

            if long is True:

                candle_close = taapi.candle(time_frame).get('close')

                if candle_close > valueLong * TAKE_PROFIT:

                    print("TAKE_PROFIT: " + str(valueLong * TAKE_PROFIT))
                    telegram_bot_sendtext("TAKE_PROFIT: " + str(valueLong * TAKE_PROFIT))

                    if LIVE:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_MARKET,
                            quantity=QUANTITY,
                        )

                    long = False

                if candle_close < valueLong * STOP_LOSS:

                    print("STOP LOSS: " + str(valueLong * STOP_LOSS))
                    telegram_bot_sendtext("STOP LOSS: " + str(valueLong * STOP_LOSS))

                    if LIVE:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_MARKET,
                            quantity=QUANTITY,
                        )

                    long = False

            sleep(30)
