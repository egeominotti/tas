import json
import logging
from backtest.services.util import find_prev_candle

logger = logging.getLogger(__name__)


def logicentry_first_long(item, bot=False):
    if bot:

        """
        item = {
            'symbol': self.symbol,
            'time_frame': self.time_frame,
            'ratio': self.func_entry.ratio,
            'stop_loss': self.func_exit.stop_loss,
            'take_profit': self.func_exit.take_profit,
            'sleep_func_entry': self.func_exit.sleep,
            'sleep_func_exit': self.func_exit.sleep,
            'taapi': self.taapi,
            'candle_close': value
        }
        """
        print(item)
        time_frame = item['time_frame']
        taapi = item['taapi']
        canlde_close = item['candle_close']

        ema8_prev = taapi.ema(8, time_frame, 1).get('value')
        candle_low_prev = taapi.candle(time_frame, 1).get('low')
        candle_open_prev = taapi.candle(time_frame, 1).get('open')

        ema8 = taapi.ema(8, time_frame)
        ema13 = taapi.ema(13, time_frame)
        ema21 = taapi.ema(21, time_frame)
        ema34 = taapi.ema(34, time_frame)

        if ema8 > ema13:
            if ema13 > ema21:
                if ema21 > ema34:
                    if candle_low_prev <= ema8_prev:
                        if canlde_close > candle_open_prev:
                            return True

    else:
        """
        Casistica usata dal backtesting
        """

        prev_item = find_prev_candle(item, 1)
        prev_indicators = json.loads(prev_item.indicators)

        if item['ema8'] > item['ema13'] > item['ema21'] > item['ema34']:
            if prev_item.low <= prev_indicators['ema8']:
                if item['close'] > prev_item.open:
                    return True
        return False


def logicexit_first_long(item, bot=False):
    if bot:

        """
        item = {
            'symbol': self.symbol,
            'time_frame': self.time_frame,
            'ratio': self.func_entry.ratio,
            'stop_loss': self.func_exit.stop_loss,
            'take_profit': self.func_exit.take_profit,
            'sleep_func_entry': self.func_exit.sleep,
            'sleep_func_exit': self.func_exit.sleep,
            'taapi': self.taapi
        }
        """
        print(item)

        if item['candle_close'] >= item['entry_candle'] * item['take_profit']:
            item['is_take_profit'] = True
            return True

        if item['candle_close'] <= item['entry_candle'] * item['stop_loss']:
            item['is_stop_loss'] = True
            return True

        return False

    else:

        if item['close_candle'] >= item['open_candle'] * item['take_profit']:
            return True

        if item['close_candle'] <= item['open_candle'] * item['stop_loss']:
            return True
        return False
