def logicentry_bot_rsi_20_bollinger(item: dict) -> None:
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

    if rsi < 20 and item['candle_close'] <= valueLowerBand:
        item['type'] = 0  # type = 0 corrisponde ad una entrata long
        item['entry'] = True
        item['entry_candle'] = item['candle_close']

    # Short only in futures market
    if item.get('market') == 'FUTURES':

        #if rsi > 85 and item['candle_close'] >= valueUpperBand:
        if rsi > 40:
            item['type'] = 1  # type = 1 corrisponde ad una entrata short
            item['entry'] = True
            item['entry_candle'] = item['candle_close']


def logicexit_bot_rsi_20_bollinger(item: dict) -> None:
    # indicators = item['indicators']
    # item['candle_close'] = indicators.candle().get('close')

    print("symbol: " + str(item.get('symbol_exchange'))
          + " Market: " + str(item.get('market'))
          + " time_frame:" + str(item.get('time_frame'))
          + " candle_close:" + str(item['candle_close'])
          )
    # + " valueLowerBand:" + str(indicators.bbands(20).get('valueLowerBand'))
    # + " valueUpperBand:" + str(indicators.bbands(20).get('valueUpperBand')))

    # bbands = indicators.bbands(20)
    # valueUpperBand = bbands.get('valueUpperBand')
    # valueLowerBand = bbands.get('valueLowerBand')

    # Market Spot
    if item.get('market') == 'SPOT':

        if item['type'] == 0:

            if item['candle_close'] >= item['entry_candle'] * item['takeprofit_value_long']:
                item['takeprofit_candle'] = item['candle_close']
                item['takeprofit'] = True

            if item['candle_close'] <= item['entry_candle'] * item['stoploss_value_long']:
                item['stoploss_candle'] = item['candle_close']
                item['stoploss'] = True

    # Market Futures
    if item.get('market') == 'FUTURES':

        # Long
        if item['type'] == 0:

            if item['candle_close'] >= item['entry_candle'] * item['takeprofit_value_long']:
                item['takeprofit_candle'] = item['candle_close']
                item['takeprofit'] = True

            if item['candle_close'] <= item['entry_candle'] * item['stoploss_value_long']:
                item['stoploss_candle'] = item['candle_close']
                item['stoploss'] = True

        # Short
        else:

            if item['candle_close'] <= item['entry_candle'] * item['takeprofit_value_short']:
                item['takeprofit_candle'] = item['candle_close']
                item['takeprofit'] = True

            if item['candle_close'] >= item['entry_candle'] * item['stoploss_value_short']:
                item['stoploss_candle'] = item['candle_close']
                item['stoploss'] = True
