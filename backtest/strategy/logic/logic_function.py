import json
import logging
import datetime
from time import sleep
from analytics.model.indicator import btby_momentum
from backtest.services.util import find_prev_candle
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy

logger = logging.getLogger(__name__)

"""
{
    'candle_close': 0,
    'entry_candle': 0,
    'takeprofit_ratio': 0,
    'takeprofit_candle': 0,
    'takeprofit': False,
    'stoploss_ratio': 0,
    'stoploss_candle': 0,
    'stoploss': False,
    'entry': False,
    'sleep_func_entry': self.func_entry.sleep,
    'taapi': self.taapi,
    'symbol': self.symbol,
    'symbol_exchange': self.symbol_exchange,
    'type': -1,
    'time_frame': self.time_frame,
    'ratio': self.func_entry.ratio,
    'stoploss_value': self.func_exit.stop_loss,
    'takeprofit_value': self.func_exit.take_profit,
    'entry_function': False,
    'exit_function': False,
    'user': self.user.username
    }
"""
"""
{
    'sleep_func_entry': Funzione della stratrgia di entry che viene valuta per essere eseguita,
    'sleep_func_exit': Funzione della strategia di exit che viene valutata per essere eseguita,
    'taapi': Instanza di taapi per prelevare i dati,
    'symbol': Simbolo da tradare preso dalla strategia,
    'type': Tipologia di strategia long or short,
    'time_frame': Valore timeframe preso dalla strategia,
    'ratio': Valore del ratio presto dalla funzione della strategia,
    'stoploss_value': Valore stoploss preso dalla funzione della strategia,
    'takeprofit_value': Valore dello stop loss preso dalla funzione della strategia,
    'takeprofit': Determina se c'e stato un takeprofit,
    'takeprofit_candle': Valore della candela di takeprofit,
    'stoploss': Determina se c'e stato uno stop loss,
    'stoploss_candle': Valore della candela di stop loss,
    'entry': Determina se è stata trovata un'entry,
    'entry_candle': Candela che viene salvata quando avviene un'entry,
    'entry_function': Determina se è passato in quella determinata funzione,
    'exit_function': Determina se è passato in quella determinata funzione
}
"""


def logicentry_first(item, bot=False):
    if bot:

        item['candle_close'] = item.get('taapi').candle(item.get('time_frame')).get('close')
        item['long_short_ratio'] = btby_momentum(item.get('symbol_exchange').replace('USDT', ''))
        longShortRatio = item['long_short_ratio']
        time_frame = item['time_frame']
        taapi = item['taapi']
        canlde_close = item['candle_close']

        ema8_prev = taapi.ema(8, time_frame, 2).get('value')
        candle_low_prev = taapi.candle(time_frame, 2).get('low')
        candle_high_prev = taapi.candle(time_frame, 2).get('high')
        candle_open_prev = taapi.candle(time_frame, 2).get('open')

        ema8 = taapi.ema(8, time_frame)
        ema13 = taapi.ema(13, time_frame)
        ema21 = taapi.ema(21, time_frame)
        ema34 = taapi.ema(34, time_frame)

        print(datetime.datetime.now())
        print("CANDLE CLOSE: " + str(canlde_close))
        print("CANDLE OPEN PREV:" +str(candle_open_prev))
        print("CANDLE HIGH PREV:" +str(candle_high_prev))
        print("CANDLE LOW PREV:" +str(candle_low_prev))

        if longShortRatio is not None and longShortRatio > 1:

            print("ENTRO LONG")

            """
            LONG entry
            """

            if ema8 > ema13:
                if ema13 > ema21:
                    if ema21 > ema34:
                        if candle_low_prev <= ema8_prev:
                            if ema8 / ema13 < 1.00165 and ema21 / ema34 < 1.00095:
                                if canlde_close > candle_open_prev:
                                    item['type'] = 0  # type = 0 corrisponde ad una entrata long
                                    item['entry'] = True
                                    item['entry_candle'] = item['candle_close']
                                    return True

        elif longShortRatio is not None and longShortRatio < 1:

            print("ENTRO SHORT")

            """
            SHORT entry
            """

            if ema8 < ema13:
                if ema13 < ema21:
                    if ema21 < ema34:
                        if candle_high_prev >= ema8_prev:
                            if ema34 / ema21 < 1.0006 and ema13 / ema8 < 1.0009:
                                if canlde_close < candle_open_prev:
                                    item['type'] = 1  # type = 1 corrisponde ad una entrata short
                                    item['entry'] = True
                                    item['entry_candle'] = item['candle_close']
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


def logicexit_first(item, bot=False):
    if bot:

        #binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        binance_websocket_api_manager.create_stream(['kline_1m'], [item.get('symbol_exchange').lower()],output="UnicornFy")

        try:
            while True:

                sentinel = False
                oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
                if oldest_stream_data_from_stream_buffer:
                    binance_stream = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
                    for k, v in binance_stream.items():
                        if isinstance(v, dict):
                            # v.get('open_price')
                            # v.get('close_price')
                            # v.get('low_price')
                            # v.get('high_price')
                            # v.get('is_closed')
                            item['candle_close'] = float(v.get('close_price'))

                    if item['type'] == 0:

                        """
                        LONG
                        """

                        if item['candle_close'] >= item['entry_candle'] * item['takeprofit_value_long']:
                            item['takeprofit_candle'] = item['candle_close']
                            item['takeprofit'] = True
                            sentinel = True
                            break

                        if item['candle_close'] <= item['entry_candle'] * item['stoploss_value_long']:
                            item['stoploss_candle'] = item['candle_close']
                            item['stoploss'] = True
                            sentinel = True
                            break

                    else:

                        """
                        SHORT
                        """

                        if item['candle_close'] <= item['entry_candle'] * item['takeprofit_value_short']:
                            item['takeprofit_candle'] = item['candle_close']
                            item['takeprofit'] = True
                            sentinel = True
                            break

                        if item['candle_close'] >= item['entry_candle'] * item['stoploss_value_short']:
                            item['stoploss_candle'] = item['candle_close']
                            item['stoploss'] = True
                            sentinel = True
                            break

                #sleep(1)

        except Exception as e:
            return e

        if sentinel is True:
            return sentinel
        return False

    else:

        if item['close_candle'] >= item['open_candle'] * item['take_profit']:
            return True

        if item['close_candle'] <= item['open_candle'] * item['stop_loss']:
            return True

        return False
