import json
import logging
from backtest.services.util import find_prev_candle

logger = logging.getLogger(__name__)


def logicentry_first(item):


    print(item)
    prev_item = find_prev_candle(item, 1)
    print(prev_item)
    prev_indicators = json.loads(prev_item.indicators)

    if item['ema8'] > item['ema13'] > item['ema21'] > item['ema34']:
        if prev_item.low <= prev_indicators['ema8']:
            if item['close'] > prev_item.open:
                return True
    return False


def logicexit_first(item):

    if item['close_candle'] >= item['open_candle'] * item['take_profit']:
        item['takeprofit_func'] = True
        return True

    if item['close_candle'] <= item['open_candle'] * item['stop_loss']:
        item['stoploss_func'] = True
        return True

    return False
