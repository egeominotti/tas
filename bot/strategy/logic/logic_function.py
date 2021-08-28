import logging

logger = logging.getLogger(__name__)


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

    rsi = indicators.rsi(14)
    bbands = indicators.bbands(20)

    item['candle_close'] = indicators.candle().get('close')

    print("symbol: " + str(item.get('symbol_exchange'))
          + " Market: " + str(item.get('market'))
          + " Time Frame : " + str(item.get('time_frame'))
          + " Candle Close: " + str(item['candle_close'])
          + " RSI: " + str(rsi)
          + " valueLowerBand: " + str(bbands.get('valueLowerBand'))
          + " valueUpperBand: " + str(bbands.get('valueUpperBand')))

    valueLowerBand = bbands.get('valueLowerBand')
    valueUpperBand = bbands.get('valueUpperBand')

    if rsi < 21 and item['candle_close'] <= valueLowerBand:
        item['type'] = 0  # type = 0 corrisponde ad una entrata long
        item['entry'] = True
        item['entry_candle'] = item['candle_close']

    # Short only in futures market
    if item.get('market') == 'FUTURES':

        if rsi > 85 and item['candle_close'] >= valueUpperBand:
            item['type'] = 1  # type = 1 corrisponde ad una entrata short
            item['entry'] = True
            item['entry_candle'] = item['candle_close']


def logicexit_bot_rsi_20_bollinger(item):

    indicators = item['indicators']
    item['candle_close'] = indicators.candle().get('close')

    print("symbol: " + str(item.get('symbol_exchange'))
          + " Market: " + str(item.get('market'))
          + " time_frame:" + str(item.get('time_frame'))
          + " candle_close:" + str(item['candle_close'])
          + " valueLowerBand:" + str(indicators.bbands(20).get('valueLowerBand'))
          + " valueUpperBand:" + str(indicators.bbands(20).get('valueUpperBand')))

    bbands = indicators.bbands(20)
    valueUpperBand = bbands.get('valueUpperBand')
    valueLowerBand = bbands.get('valueLowerBand')

    if item.get('market') == 'SPOT':

        if item['type'] == 0:

            if item['candle_close'] >= valueUpperBand * 0.993:
                item['takeprofit_candle'] = item['candle_close']
                item['takeprofit'] = True

            if item['candle_close'] <= item['entry_candle'] * item['stoploss_value_long']:
                item['stoploss_candle'] = item['candle_close']
                item['stoploss'] = True

    if item.get('market') == 'FUTURES':

        # Long
        if item['type'] == 0:

            if item['candle_close'] >= valueUpperBand * 0.993:
                item['takeprofit_candle'] = item['candle_close']
                item['takeprofit'] = True

            if item['candle_close'] <= item['entry_candle'] * item['stoploss_value_long']:
                item['stoploss_candle'] = item['candle_close']
                item['stoploss'] = True

        # Short
        else:

            if item['candle_close'] <= valueLowerBand * 0.993:
                item['takeprofit_candle'] = item['candle_close']
                item['takeprofit'] = True

            if item['candle_close'] >= item['entry_candle'] * item['stoploss_value_short']:
                item['stoploss_candle'] = item['candle_close']
                item['stoploss'] = True
