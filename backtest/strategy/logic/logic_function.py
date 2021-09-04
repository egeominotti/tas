import json
import logging
from backtest.services.util import find_prev_candle

logger = logging.getLogger(__name__)

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


