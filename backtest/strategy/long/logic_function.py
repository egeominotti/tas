import json
from dateutil.relativedelta import relativedelta
from analytics.models import Importer
from analytics.services.exchangeApi import Taapi
import logging

logger = logging.getLogger(__name__)

"""
STRATEGY : 1
"""


def logic_entry(item, bot=False):
    if bot:
        try:
            """
            Casistica usata dal bot
            """
            time_frame = item['time_frame']
            symbol = item['symbol']
            ratio = item['ratio']

            taapi = Taapi(symbol)
            candle_close = taapi.candle(time_frame).get('close')
            ema9 = taapi.ema(9, time_frame)
            ema24 = taapi.ema(24, time_frame)
            ema100 = taapi.ema(100, time_frame)

            print("sono dentro logic_entry")
            print(item)
            print("candle close:" + str(candle_close))
            print("ema9: " + str(ema9))
            print("ema 24: " + str(ema24))
            print("ema 100:" + str(ema100))

            logger.info("Sono dentro logic entry")
            logger.info("item passato a logic entry: " + str(item))
            logger.info("ema9: " + str(ema9))
            logger.info("ema 24: " + str(ema24))
            logger.info("ema 100:" + str(ema100))
            logger.info("ratio ema9/ema24:" + str(ema9 / ema24))

            #ratio_value = ema9 / ema24
            #if candle_close > ema100:
            return candle_close

        except Exception as e:
            logger.exception("Exception logic entry: " + str(e))
            return e
    else:
        """
        Casistica usata dal backtesting
        """
        ratio_value = item['ema9'] / item['ema24']
        if 1 < ratio_value < item['ratio']:
            if item['close'] > item['ema100']:
                return True
        return False


def logic_stop_loss(item, bot=False):
    if bot:
        try:
            """
            Casistica usata dal bot
            """
            time_frame = item['time_frame']
            symbol = item['symbol']
            stop_loss = item['stop_loss']
            taapi = Taapi(symbol)
            candle_close = taapi.candle(time_frame).get('close')

            print("sono dentro logic_stop_loss")
            print(item)
            print(candle_close)
            print(symbol)
            print(candle_close)

            print(item['open_position_value'] * stop_loss)
            print(candle_close <= item['open_position_value'] * stop_loss)
            if candle_close <= item['open_position_value'] * stop_loss:
                return candle_close

            return False

        except Exception as e:
            logger.exception("Exception logic stop loss: " + str(e))
            return e

    else:
        """
         Casistica usata dal backtesting
        """
        if item['close_candle'] <= item['open_candle'] * item['stop_loss']:
            return True
        return False


def logic_takeprofit(item, bot=False):
    if bot:
        try:
            """
            Casistica usata dal bot
            """
            time_frame = item['time_frame']
            symbol = item['symbol']
            take_profit = item['take_profit']
            taapi = Taapi(symbol)
            candle_close = taapi.candle(time_frame).get('close')

            print("sono dentro logic_takeprofit")
            print(item)
            print(symbol)
            print(candle_close)

            if candle_close >= item['open_position_value'] * take_profit:
                return candle_close

            return False

        except Exception as e:
            logger.exception("Exception logic take profit: " + str(e))
            return e
    else:
        """
         Casistica usata dal backtesting
        """
        print(item['close_candle'] >= item['open_candle'] * item['take_profit'])
        print(item['open_candle'] * item['take_profit'])
        if item['close_candle'] >= item['open_candle'] * item['take_profit']:
            return True
        return False


"""
STRATEGY : 2
"""

#
# def scalping_5m_rsi_bollinger(item, bot=False) -> bool:
#     if bot:
#         ratio = item['ratio']
#         ratio_value = item['bbands']['valueMiddleBand'] / item['bbands']['valueLowerBand']
#         if ratio_value >= ratio:
#             if item['rsi']['value'] > 30:
#                 return True
#     else:
#         prev = item['timestamp'] - relativedelta(days=1)
#         qs = Importer.objects.get(tf='1d', timestamp=item['timestamp'])
#         indicatos = json.loads(qs.indicators)
#
#         print(prev)
#         print(indicatos['rsi'])
#         print(item['timestamp'])
#         print(item['rsi'])
#
#         ratio_value = item['middleband'] / item['lowerband']
#         if ratio_value >= item['ratio']:
#             if item['rsi'] > 30:
#                 return True
#
#     return False
#
#
# def stoploss_scalping_5m_rsi_bollinger(item=None, bot=False) -> bool:
#     if item['open_candle'] > item['close_candle'] * item['take_profit']:
#         return True
#     return False
#
#
# def takeprofit_scalping_5m_rsi_bollinger(item, bot=False) -> bool:
#     pass
#     # if bot:
#     #     middleband_flag = item['bbands']['valueMiddleBand'] * 1.013
#     #     if candle_close_entry >= middleband_flag or item['candle']['close'] > signal_candle_close * take_profit:
#     #         return True
#     # else:
#     #     middleband_flag = item['middleband'] * 1.013
#     #     if candle_close_entry >= middleband_flag or item['close'] > signal_candle_close * take_profit:
#     #         return True
#     # return False
