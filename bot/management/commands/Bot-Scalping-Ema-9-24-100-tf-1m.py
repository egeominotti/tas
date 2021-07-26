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
client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))
client.futures_change_leverage(symbol='BTCUSDT', marginType='ISOLATED', leverage=1)


# https://api.telegram.org/bot1889367095:AAGS13rjA6xWAGvcUTOy1W1vUZvPnNxcDaw/getUpdates
def telegram_bot_sendtext(bot_message):
    bot_token = '1889367095:AAGS13rjA6xWAGvcUTOy1W1vUZvPnNxcDaw'
    bot_chatID = '-558016221'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def get_quantity_precision(currency_symbol):
    info = client.futures_exchange_info()
    info = info['symbols']
    for x in range(len(info)):
        if info[x]['symbol'] == currency_symbol:
            return info[x]['pricePrecision']
    return None


class Command(BaseCommand):
    help = 'Bot-Scalping-Ema-9-24-100-15min'

    def handle(self, *args, **kwargs):

        # 20 USDT
        TRADE_SIZE = 30.0

        TYPE = 'LONG'
        TAKE_PROFIT = 1.01
        STOP_LOSS = 0.995
        RATIO = 1.00005
        time_frame = '1m'
        QUANTITY = 0.002
        valueLong = 0
        ema1 = 5
        ema2 = 10
        ema3 = 60
        LIVE = False
        sentinel = False
        TELEGRAM_BOT = False

        txt = "\n-Strategy: " + str(TYPE) + "\n-Timeframe: " + str(time_frame) + "\n -Ema1: " + str(
            ema1) + "\n-Ema2: " + str(ema2) + "\n -Ema3: " + str(
            ema3) + "\n-Take_profit_value: " + str(TAKE_PROFIT) + "\n-Stop_loss_value: " + str(STOP_LOSS)
        if TELEGRAM_BOT:
            telegram_bot_sendtext(txt)

        taapi = Taapi('BTC/USDT')

        price = client.get_symbol_ticker(symbol="BTCUSDT")
        print(price)
        QUANTITY = TRADE_SIZE / float(price.get('price'))

        info = client.get_account()
        print(info)
        # set the percentage or fraction you want to invest in each order

        while True:

            candle_close = taapi.candle(time_frame).get('close')
            if candle_close is None:
                if TELEGRAM_BOT:
                    telegram_bot_sendtext("Errore nei dati esco dal bot")
                break

            if sentinel is False:

                ema1 = taapi.ema(ema1, time_frame)
                ema2 = taapi.ema(ema2, time_frame)
                ema3 = taapi.ema(ema3, time_frame)

                if ema1 is None or ema2 is None or ema3 is None:
                    if TELEGRAM_BOT:
                        telegram_bot_sendtext("Errore nei dati esco dal bot")
                    break

                ratio_value = ema1 / ema2
                if 1 < ratio_value < RATIO:
                    if candle_close > ema3:

                        s0 = "Time frame: " + str(time_frame)
                        s1 = "Compro al prezzo: " + str(candle_close)
                        s2 = "TP: " + str(candle_close * TAKE_PROFIT)
                        s3 = "SL: " + str(candle_close * STOP_LOSS)

                        if TELEGRAM_BOT:
                            telegram_bot_sendtext(s0 + "\n" + s1 + "\n" + s2 + "\n" + s3)

                        print("---------------------------------------------------")
                        print(s0)
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
                        sentinel = True
                sleep(59)

            if sentinel is True:

                candle_close = taapi.candle('1m').get('close')
                if candle_close is None:
                    if TELEGRAM_BOT:
                        telegram_bot_sendtext("Errore nei dati esco dal bot")
                    break

                if candle_close > valueLong * TAKE_PROFIT:

                    print("TAKE_PROFIT: " + str(valueLong * TAKE_PROFIT))
                    if TELEGRAM_BOT:
                        telegram_bot_sendtext("TAKE_PROFIT: " + str(valueLong * TAKE_PROFIT))

                    if LIVE:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_MARKET,
                            quantity=QUANTITY,
                        )

                    sentinel = False

                if candle_close < valueLong * STOP_LOSS:

                    print("STOP LOSS: " + str(valueLong * STOP_LOSS))
                    if TELEGRAM_BOT:
                        telegram_bot_sendtext("STOP LOSS: " + str(valueLong * STOP_LOSS))

                    if LIVE:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_MARKET,
                            quantity=QUANTITY,
                        )

                    sentinel = False

                # if TELEGRAM_BOT:
                #     telegram_bot_sendtext(
                #         "Time frame del bot: \n" + str(time_frame) + " - posizione aperta con valore: \n" + str(
                #             valueLong) + "\n - valore candela ad un minuto close: " + str(candle_close))
                sleep(59)
