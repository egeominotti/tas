import json
from dateutil.relativedelta import relativedelta
from analytics.models import Importer
from analytics.services.exchangeApi import Taapi

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
            candle_close = taapi.candle(time_frame)
            ema9 = taapi.ema(9, time_frame)
            ema24 = taapi.ema(24, time_frame)
            ema100 = taapi.ema(100, time_frame)

            ratio_value = ema9 / ema24
            if 1 < ratio_value < ratio:
                if candle_close['close'] > ema100:
                    return candle_close
            return False
        except Exception as e:
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
            candle_close = taapi.candle(time_frame)
            if item['open_position_value'] < candle_close * stop_loss:
                return True
            return False

        except Exception as e:
            return e
    else:
        """
         Casistica usata dal backtesting
        """
        if item['open_candle'] < item['close_candle'] * item['stop_loss']:
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
            candle_close = taapi.candle(time_frame)
            if item['open_position_value'] > candle_close * take_profit:
                return True
            return False
        except Exception as e:
            return e
    else:
        """
         Casistica usata dal backtesting
        """
        if item['open_candle'] > item['close_candle'] * item['take_profit']:
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
