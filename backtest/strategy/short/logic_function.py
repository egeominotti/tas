from time import sleep

import json

from analytics.services.exchangeApi import Taapi
import logging
from backtest.services.util import find_prev_candle

logger = logging.getLogger(__name__)


def logic_entry_ema8_13_21_34(item, bot=False):
    if bot:

        try:

            symbol = item['symbol']
            taapi = Taapi(symbol)
            ratio = item['ratio']
            time_frame = item['time_frame']

            ema8 = taapi.ema(8, time_frame)

            ema8_prev = taapi.ema(8, time_frame, 1)
            candle_close_prev = taapi.candle(time_frame, 1).get('close')
            candle_open_prev = taapi.candle(time_frame, 1).get('close')

            candle_close = taapi.candle(time_frame).get('close')
            ema13 = taapi.ema(13, time_frame)
            ema21 = taapi.ema(21, time_frame)
            ema34 = taapi.ema(34, time_frame)

            if ema8 < ema13 < ema21 < ema34:
                if candle_close_prev >= ema8_prev:
                    if candle_close < candle_open_prev:
                        return candle_close

        except Exception as e:
            logger.exception("Exception logic entry: " + str(e))
            return e
    else:
        """
        Casistica usata dal backtesting
        """
        prev_item = find_prev_candle(item, 1)
        prev_indicators = json.loads(prev_item.indicators)

        if item['ema8'] < item['ema13'] < item['ema21'] < item['ema34']:
            if prev_item.high >= prev_indicators['ema8']:
                if item['close'] < prev_item.open:
                    return True
        return False


def logic_ema8_13_21_34_takeprofit(item, bot=False):
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

            if candle_close >= item['open_position_value'] * take_profit:
                return candle_close

            return False

        except Exception as e:
            logger.exception("Exception logic take profit: " + str(e))
            return e
    else:
        print(item['close_candle'] >= item['open_candle'] * item['take_profit'])
        print(item['open_candle'] * item['take_profit'])
        if item['close_candle'] >= item['open_candle'] * item['take_profit']:
            return True
        return False


def logic_ema8_13_21_34_stop_loss(item, bot=False):
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

            if candle_close <= item['open_position_value'] * stop_loss:
                return candle_close

            return False

        except Exception as e:
            logger.exception("Exception logic stop loss: " + str(e))
            return e

    else:
        if item['close_candle'] <= item['open_candle'] * item['stop_loss']:
            return True
        return False
