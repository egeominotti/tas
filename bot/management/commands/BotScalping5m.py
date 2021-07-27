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

        take_profit = 1.02
        stop_loss = 0.98
        ratio = 1.0098
        time_frame = '5m'
        quantity = 0.004

        live = False
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

            if open_position is False:

                candle_close = taapi.candle(time_frame).get('close')
                if candle_close is None:
                    telegram_bot_sendtext("Errore nei dati esco dal bot")
                    break

                sleep(5)
                rsi = taapi.rsi(time_frame)
                bbands = taapi.bbands(time_frame)
                print(rsi)
                print(bbands)

                item = {
                    'rsi': rsi.get('value'),
                    'middleband': bbands.get('valueMiddleBand'),
                    'lowerband': bbands.get('valueLowerBand')
                }

                if scalping_5m_rsi_bollinger(item, ratio):

                    s0 = "Time frame: " + time_frame
                    s1 = "Compro al prezzo: " + str(candle_close)
                    s2 = "TP: " + str(candle_close * take_profit)
                    s3 = "SL: " + str(candle_close * stop_loss)

                    telegram_bot_sendtext(s0 + "\n" + s1 + "\n" + s2 + "\n" + s3)

                    print("---------------------------------------------------")
                    print(s1)
                    print(s2)
                    print(s3)
                    print("---------------------------------------------------")

                    if live:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_BUY,
                            type=ORDER_TYPE_MARKET,
                            quantity=quantity,
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

                if takeprofit_scalping_5m_rsi_bollinger(open_position_value, candle_close, take_profit, item):

                    print("TAKE_PROFIT: " + str(open_position_value * take_profit))
                    telegram_bot_sendtext("TAKE_PROFIT: " + str(open_position_value * take_profit))

                    if live:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_MARKET,
                            quantity=quantity,
                        )

                    break

                if stoploss_scalping_5m_rsi_bollinger(open_position_value, candle_close, stop_loss):

                    print("STOP LOSS: " + str(open_position_value * stop_loss))
                    telegram_bot_sendtext("STOP LOSS: " + str(open_position_value * stop_loss))

                    if live:
                        client.futures_create_order(
                            symbol='BTCUSDT',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_MARKET,
                            quantity=quantity,
                        )

                    break

                sleep(300)
