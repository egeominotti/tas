import json
import logging
from backtest.services.util import find_prev_candle

logger = logging.getLogger(__name__)


"""
STRATEGY 2: RSI 20 BOLLINGER
"""

def logicentry_backtest_rsi_20_bollinger(item):

    rsi = item['rsi']
    bband_lower = item['lowerband']
    print(item)
    if rsi < 20 and item['close'] <= bband_lower:
        return True

    return False



def logicexit_backtest_rsi_20_bollinger(item):

    bband_upper = item['upperband']

    if item['close'] >= bband_upper:
        item['takeprofit_func'] = True
        return True
    print(item)
    if item['close'] <= item['open'] * item['stoploss']:
        item['stoploss_func'] = True
        return True

    return False

def logicentry_backtest_first(item):


    prev_item = find_prev_candle(item, 1)
    prev_indicators = json.loads(prev_item.indicators)

    if item['ema8'] > item['ema13'] > item['ema21'] > item['ema34']:
        if prev_item.low <= prev_indicators['ema8']:
            if item['close'] > prev_item.open:
                return True
    return False


def logicexit_backtest_first(item):

    if item['close'] >= item['open'] * item['take_profit']:
        item['takeprofit_func'] = True
        return True

    if item['close'] <= item['open'] * item['stop_loss']:
        item['stoploss_func'] = True
        return True

    return False
