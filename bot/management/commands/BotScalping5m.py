from binance.enums import *
from binance import Client
from decouple import config
from time import sleep
from analytics.services.exchangeApi import Taapi
from django.core.management import BaseCommand
import requests
import logging
from django.conf import settings
from backtest.strategy.long.logic_function import logic_entry, logic_stop_loss, logic_takeprofit, \
    scalping_5m_rsi_bollinger, stoploss_scalping_5m_rsi_bollinger, takeprofit_scalping_5m_rsi_bollinger

logger = logging.getLogger('main')


# https://api.telegram.org/bot1889367095:AAGS13rjA6xWAGvcUTOy1W1vUZvPnNxcDaw/getUpdates
def telegram_bot_sendtext(bot_message):
    bot_token = '1889367095:AAGS13rjA6xWAGvcUTOy1W1vUZvPnNxcDaw'
    bot_chatID = '-558016221'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


class Command(BaseCommand):
    help = 'BotScalping5m'

    def handle(self, *args, **kwargs):

        TAKE_PROFIT = 1.98
        STOP_LOSS = 0.98
        RATIO = 1.009
        time_frame = '1m'
        QUANTITY = 0.004

        LIVE = False
        open_position = False

        taapi = Taapi('BTC/USDT')
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))
        client.futures_change_leverage(symbol='BTCUSDT', marginType='ISOLATED', leverage=1)

        telegram_bot_sendtext("\n")
        telegram_bot_sendtext("\n")


        txt = "BOT: Started"
        telegram_bot_sendtext(txt)
        open_position_value = 0
        while True:

            candle_close = taapi.candle(time_frame).get('close')
            if candle_close is None:
                telegram_bot_sendtext("Errore nei dati esco dal bot")
                break

            if open_position is False:

                rsi = taapi.rsi(time_frame)
                bbands = taapi.bbands(time_frame)

                item = {
                    'rsi': rsi.get('value'),
                    'middleband': bbands.get('valueMiddleBand'),
                    'lowerband': bbands.get('valueLowerBand')
                }

                if scalping_5m_rsi_bollinger(item, RATIO):

                    s0 = "Time frame: " + time_frame
                    s1 = "Compro al prezzo: " + str(candle_close)
                    s2 = "TP: " + str(candle_close * TAKE_PROFIT)
                    s3 = "SL: " + str(candle_close * STOP_LOSS)

                    telegram_bot_sendtext(s0 + "\n" + s1 + "\n" + s2 + "\n" + s3)

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

                    open_position_value = candle_close
                    open_position = True

                    break

                sleep(300)

        if open_position is True:
            while True:

                candle_close = taapi.candle(time_frame).get('close')
                bbands = taapi.bbands(time_frame)

                item = {
                    'middleband': bbands.get('valueMiddleBand'),
                    'lowerband': bbands.get('valueLowerBand'),
                    'close': candle_close
                }
                print(item)

                if takeprofit_scalping_5m_rsi_bollinger(open_position_value, candle_close, TAKE_PROFIT, item):

                    print("TAKE_PROFIT: " + str(open_position_value * TAKE_PROFIT))
                    telegram_bot_sendtext("TAKE_PROFIT: " + str(open_position_value * TAKE_PROFIT))

                    if LIVE:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_MARKET,
                            quantity=QUANTITY,
                        )

                    break

                if stoploss_scalping_5m_rsi_bollinger(open_position_value, candle_close, STOP_LOSS):

                    print("STOP LOSS: " + str(open_position_value * STOP_LOSS))
                    telegram_bot_sendtext("STOP LOSS: " + str(open_position_value * STOP_LOSS))

                    if LIVE:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_MARKET,
                            quantity=QUANTITY,
                        )

                    break

                sleep(300)
