def logic_entry(item, ratio) -> bool:
    ratio_value = item['ema9'] / item['ema24']
    if 1 < ratio_value < ratio:
        if item['close'] > item['ema100']:
            return True
    return False


def logic_stop_loss(candle_close_entry, signal_candle_close, stop_loss, item) -> bool:
    if candle_close_entry < signal_candle_close * stop_loss:
        return True
    return False


def logic_takeprofit(candle_close_entry, signal_candle_close, take_profit, item) -> bool:
    if candle_close_entry > signal_candle_close * take_profit:
        return True
    return False


def scalping_5m_rsi_bollinger(item, ratio) -> bool:

    ratio_value = item['middleband'] / item['lowerband']

    if ratio_value >= ratio:
        if item['rsi'] > 30:
            return True
    return False


def stoploss_scalping_5m_rsi_bollinger(candle_close_entry, signal_candle_close, stop_loss, item=None) -> bool:

    if candle_close_entry < signal_candle_close * stop_loss:
        return True
    return False


def takeprofit_scalping_5m_rsi_bollinger(candle_close_entry, signal_candle_close, take_profit, item=None) -> bool:
    middleband_flag = item['middleband'] * 1.011

    if candle_close_entry >= middleband_flag or item['close'] > signal_candle_close * take_profit:
        return True
    return False
