import json
import logging
from analytics.services.exchangeApi import Taapi
from backtest.services.util import find_prev_candle

logger = logging.getLogger(__name__)


def logic_entry_ema8_13_21_34_long(item, bot=False):
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
        }
        """

        time_frame = item['time_frame']
        taapi = Taapi(['symbol'])

        ema8_prev = taapi.ema(8, time_frame, 1).get('value')
        candle_low_prev = taapi.candle(time_frame, 1).get('low')
        candle_open_prev = taapi.candle(time_frame, 1).get('open')
        candle_close = taapi.candle(time_frame).get('close')

        ema8 = taapi.ema(8, time_frame)
        ema13 = taapi.ema(13, time_frame)
        ema21 = taapi.ema(21, time_frame)
        ema34 = taapi.ema(34, time_frame)

        if ema8 > ema13:
            if ema13 > ema21:
                if ema21 > ema34:
                    if candle_low_prev <= ema8_prev:
                        if candle_close > candle_open_prev:
                            return candle_close

    else:
        """
        Casistica usata dal backtesting
        """

        """
        Sistema per accedere 
        """
        prev_item = find_prev_candle(item, 1)
        prev_indicators = json.loads(prev_item.indicators)

        if item['ema8'] > item['ema13'] > item['ema21'] > item['ema34']:
            if prev_item.low <= prev_indicators['ema8']:
                if item['close'] > prev_item.open:
                    return True
        return False


def logic_exit_ema8_13_21_34_long(item, bot=False):
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
        }
        """

        taapi = Taapi(item['symbol'])
        time_frame = item['time_frame']
        stop_loss = item['stop_loss']
        take_profit = item['take_profit']

        candle_close = taapi.candle(time_frame).get('close')

        if candle_close >= item['open_position_value'] * take_profit:
            return candle_close

        if candle_close <= item['open_position_value'] * stop_loss:
            return candle_close

        return False

    else:

        if item['close_candle'] >= item['open_candle'] * item['take_profit']:
            return True

        if item['close_candle'] <= item['open_candle'] * item['stop_loss']:
            return True
        return False
