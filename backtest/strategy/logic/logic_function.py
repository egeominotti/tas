import json
import logging
from backtest.services.util import find_prev_candle

logger = logging.getLogger(__name__)

"""
STRATEGY 3: EMA 60 / EMA 222
"""


def logicentry_long_backtest_ema60_ema223(item):

    ema60 = item['ema60']
    ema223 = item['ema223']

    if ema60 > ema223:
        return True

    return False


def logicexit_long_backtest_ema60_ema223(item):

    if item['close'] >= item['open'] * item['takeprofit']:
        item['takeprofit_func'] = True
        return True

    if item['close'] <= item['open'] * item['stoploss']:
        item['stoploss_func'] = True
        return True

    return False


def logicentry_short_backtest_ema60_ema223(item):

    ema60 = item['ema60']
    ema223 = item['ema223']

    if ema60 < ema223:
        return True

    return False


def logicexit_short_backtest_ema60_ema223(item):
    if item['close'] <= item['open'] * item['takeprofit']:
        item['takeprofit_func'] = True
        return True

    if item['close'] >= item['open'] * item['stoploss']:
        item['stoploss_func'] = True
        return True

    return False


"""
STRATEGY 2: RSI 20 BOLLINGER
"""


def logicentry_long_backtest_rsi_20_bollinger(item):
    rsi = item['rsi']
    bband_lower = item['lowerband']
    if rsi < 20 and item['close'] <= bband_lower:
        return True

    return False


def logicexit_long_backtest_rsi_20_bollinger(item):
    bband_upper = item['upperband']

    if item['close'] >= bband_upper:
        item['takeprofit_func'] = True
        return True

    if item['close'] <= item['entry'] * item['stoploss']:
        item['stoploss_func'] = True
        return True

    return False


def logicentry_short_backtest_rsi_20_bollinger(item):
    rsi = item['rsi']
    upperband = item['upperband']
    if rsi > 80 and item['close'] >= upperband:
        return True

    return False


def logicexit_short_backtest_rsi_20_bollinger(item):
    lowerband = item['lowerband']

    if item['close'] <= lowerband:
        item['takeprofit_func'] = True
        return True

    if item['close'] <= item['entry'] * item['stoploss']:
        item['stoploss_func'] = True
        return True

    return False

"""
STRATEGY 3: MACD
"""


def logicentry_long_backtest_macd(item):
    macd = item['macd']
    macdsignal = item['macdsignal']

    macd_ratio = macd / macdsignal

    if 1 < macd_ratio < item['ratio']:
        return True

    return False


def logicexit_long_backtest_macd(item):

    ema13 = item['ema13']

    if item['close'] < ema13:
        item['takeprofit_func'] = True
        return True

    if item['close'] <= item['entry'] * item['stoploss']:
        item['stoploss_func'] = True
        return True

    return False


"""
STRATEGIA CA CAPIRE
"""


def logicentry_backtest_first(item):
    prev_item = find_prev_candle(item, '1m', 0)
    prev_indicators = json.loads(prev_item.indicators)

    if item['ema8'] > item['ema13'] > item['ema21'] > item['ema34']:
        if prev_item.low <= prev_indicators['ema8']:
            if item['close'] > prev_item.open:
                return True
    return False


def logicexit_backtest_first(item):
    if item['close'] >= item['open'] * item['takeprofit']:
        item['takeprofit_func'] = True
        return True

    if item['close'] <= item['open'] * item['stoploss']:
        item['stoploss_func'] = True
        return True

    return False
