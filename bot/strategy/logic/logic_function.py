import logging
import datetime
from time import sleep
import decouple
import json
import redis

logger = logging.getLogger(__name__)

redis = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)


def logicentry_test(item):
    key = str(item.get('symbol_exchange')) + "_" + str(item.get('time_frame'))
    value = redis.get(key)
    candle_from_websocket = json.loads(value)
    print(candle_from_websocket)

    item['type'] = 0  # type = 0 corrisponde ad una entrata long
    item['entry'] = True
    item['entry_candle'] = item['candle_close']
    return True


def logicexit_test(item):
    key = str(item.get('symbol_exchange')) + "_" + str(item.get('time_frame'))
    value = redis.get(key)
    candle_from_websocket = json.loads(value)
    print(candle_from_websocket)

    item['takeprofit_candle'] = item['candle_close']
    item['takeprofit'] = True
    return True


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


def logicentry_bot_rsi_20_bollinger(item):

    indicators = item['indicators']
    # Real time indicator disabled check only prev closed candle
    indicators.compute(False)

    candles =   indicators.candle()
    rsi =       indicators.rsi(14)
    bbands =    indicators.bbands(20)

    item['candle_close'] = candles.get('close')

    print("symbol: " + str(item.get('symbol_exchange'))
          + " time_frame:" + str(item.get('time_frame'))
          + " candle_close:" + str(candles.get('close'))
          + " RSI:" + str(rsi)
          + " valueLowerBand:" + str(bbands.get('valueLowerBand'))
          + " valueUpperBand:" + str(bbands.get('valueUpperBand')))

    valueLowerBand = bbands.get('valueLowerBand')
    valueUpperBand = bbands.get('valueUpperBand')

    if rsi < 20 and item['candle_close'] <= valueLowerBand:
        item['type'] = 0  # type = 0 corrisponde ad una entrata long
        item['entry'] = True
        item['entry_candle'] = item['candle_close']
        return True

    if rsi > 85 and item['candle_close'] >= valueUpperBand:
        item['type'] = 1  # type = 1 corrisponde ad una entrata short
        item['entry'] = True
        item['entry_candle'] = item['candle_close']
        return True

    return False


def logicexit_bot_rsi_20_bollinger(item):

    sentinel = False

    try:
        while True:

            indicators = item['indicators']
            # Real time indicator enabled
            indicators.compute(True)
            item['candle_close'] = indicators.candle().get('close')

            print("symbol: " + str(item.get('symbol_exchange'))
                  + " time_frame:" + str(item.get('time_frame'))
                  + " candle_close:" + str(indicators.candle().get('close'))
                  + " valueLowerBand:" + str(indicators.bbands(20).get('valueLowerBand'))
                  + " valueUpperBand:" + str(indicators.bbands(20).get('valueUpperBand')))

            bbands = indicators.bbands(20)

            valueUpperBand = bbands.get('valueUpperBand')
            valueLowerBand = bbands.get('valueLowerBand')

            if item['type'] == 0:

                """
                LONG
                """

                if item['candle_close'] >= valueUpperBand:
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

                if item['candle_close'] <= valueLowerBand:
                    item['takeprofit_candle'] = item['candle_close']
                    item['takeprofit'] = True
                    sentinel = True
                    break

                if item['candle_close'] >= item['entry_candle'] * item['stoploss_value_short']:
                    item['stoploss_candle'] = item['candle_close']
                    item['stoploss'] = True
                    sentinel = True
                    break

    except Exception as e:
        return e

    if sentinel is True:
        return sentinel
    return False


def logicentry_bot_first(item):
    key = item.get('symbol_exchange') + "_" + str(item.get('time_frame'))
    value = redis.get(key)
    candle_from_websocket = json.loads(value)
    print(candle_from_websocket)

    item['candle_close'] = candle_from_websocket.get('candle_close')

    # item['candle_close'] = item.get('taapi').candle(item.get('time_frame')).get('close')
    # item['candle_close'] = BufferStreamWebSocket.objects.filter(symbol__symbol=item.get('symbol_exchange'),time_frame='1m').last().close_candle

    # item['long_short_ratio'] = btby_momentum(item.get('symbol_exchange').replace('USDT', ''))
    # longShortRatio = item['long_short_ratio']
    time_frame = item['time_frame']
    taapi = item['taapi']
    canlde_close = item['candle_close']

    ema8_prev = taapi.ema(8, time_frame, 1).get('value')
    candle_low_prev = taapi.candle(time_frame, 1).get('low')
    candle_high_prev = taapi.candle(time_frame, 1).get('high')
    candle_open_prev = taapi.candle(time_frame, 1).get('open')

    ema8 = taapi.ema(8, time_frame)
    ema13 = taapi.ema(13, time_frame)
    ema21 = taapi.ema(21, time_frame)
    ema34 = taapi.ema(34, time_frame)

    print("\n")
    print(datetime.datetime.now())
    print("CANDLE CLOSE: " + str(canlde_close))
    print("CANDLE OPEN PREV:" + str(candle_open_prev))
    print("CANDLE HIGH PREV:" + str(candle_high_prev))
    print("CANDLE LOW PREV:" + str(candle_low_prev))

    """
    LONG entry
    """

    if ema8 > ema13:
        if ema13 > ema21:
            if ema21 > ema34:
                if candle_low_prev <= ema8_prev:
                    if ema8 / ema13 < 1.00165 and ema21 / ema34 < 1.00095:
                        if canlde_close > candle_open_prev:
                            print("ENTRO LONG")
                            item['type'] = 0  # type = 0 corrisponde ad una entrata long
                            item['entry'] = True
                            item['entry_candle'] = item['candle_close']
                            return True

    """
    SHORT entry
    """

    if ema8 < ema13:
        if ema13 < ema21:
            if ema21 < ema34:
                if candle_high_prev >= ema8_prev:
                    if ema34 / ema21 < 1.0006 and ema13 / ema8 < 1.0009:
                        if canlde_close < candle_open_prev:
                            print("ENTRO SHORT")
                            item['type'] = 1  # type = 1 corrisponde ad una entrata short
                            item['entry'] = True
                            item['entry_candle'] = item['candle_close']
                            return True


def logicexit_bot_first(item):
    sentinel = False
    try:
        while True:

            key = item.get('symbol_exchange') + "_" + str(item.get('time_frame'))
            value = redis.get(key)
            candle_from_websocket = json.loads(value)
            print(candle_from_websocket)

            item['candle_close'] = candle_from_websocket.get('candle_close')

            print("Candle close from binance: " + item['candle_close'])
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


    except Exception as e:
        return e

    if sentinel is True:
        return sentinel
    return False
