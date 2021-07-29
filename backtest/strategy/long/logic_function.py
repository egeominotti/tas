import json

from dateutil.relativedelta import relativedelta
from analytics.models import Importer
from analytics.services.exchangeApi import Taapi

"""
STRATEGY : 1
"""


def logic_entry(item, bot=False) -> bool:
    if bot:
        print("ok")
        taapi = Taapi(item['symbol'])
        candle_close = taapi.candle(item['time_frame'])
        ema9 = taapi.ema(item['time_frame'], 9)
        ema24 = taapi.ema(item['time_frame'], 24)
        ema100 = taapi.ema(item['time_frame'], 100)
        ratio_value = ema9 / ema24
        if 1 < ratio_value < item['ratio']:
            if candle_close['close'] > ema100:
                return True
    else:

        ratio_value = item['ema9'] / item['ema24']
        if 1 < ratio_value < item['ratio']:
            if item['close'] > item['ema100']:
                return True
    return False


def logic_stop_loss(item, bot=True) -> bool:
    print(item)
    # if candle_close_entry < signal_candle_close * stop_loss:
    #     return True
    # return False


def logic_takeprofit(item, bot=True) -> bool:
    print(item)
    # if candle_close_entry > signal_candle_close * take_profit:
    #     return True
    # return False


"""
STRATEGY : 2
"""


def scalping_5m_rsi_bollinger(item, ratio, isbot=False) -> bool:
    if isbot:
        ratio_value = item['bbands']['valueMiddleBand'] / item['bbands']['valueLowerBand']
        if ratio_value >= ratio:
            if item['rsi']['value'] > 30:
                return True
    else:
        prev = item['timestamp'] - relativedelta(days=1)
        qs = Importer.objects.get(tf='1d', timestamp=item['timestamp'])
        indicatos = json.loads(qs.indicators)

        print(prev)
        print(indicatos['rsi'])
        print(item['timestamp'])
        print(item['rsi'])

        ratio_value = item['middleband'] / item['lowerband']
        if ratio_value >= ratio:
            if item['rsi'] > 30:
                return True

    return False


def stoploss_scalping_5m_rsi_bollinger(candle_close_entry, signal_candle_close, stop_loss, item=None) -> bool:
    if candle_close_entry < signal_candle_close * stop_loss:
        return True
    return False


def takeprofit_scalping_5m_rsi_bollinger(candle_close_entry, signal_candle_close, take_profit, item=None,
                                         isbot=False) -> bool:
    if isbot:
        middleband_flag = item['bbands']['valueMiddleBand'] * 1.013
        if candle_close_entry >= middleband_flag or item['candle']['close'] > signal_candle_close * take_profit:
            return True
    else:
        middleband_flag = item['middleband'] * 1.013
        if candle_close_entry >= middleband_flag or item['close'] > signal_candle_close * take_profit:
            return True
    return False
