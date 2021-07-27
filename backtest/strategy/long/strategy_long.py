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
