from datetime import datetime
from dateutil.relativedelta import relativedelta

from binance import Client
from decouple import config

from backtest.services.computedata import compute_data


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


def scalping_5m_rsi_bollinger(item, ratio, isbot=False) -> bool:
    if isbot:
        ratio_value = item['bbands']['valueMiddleBand'] / item['bbands']['valueLowerBand']
        if ratio_value >= ratio:
            if item['rsi']['value'] > 30:
                return True
    else:
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))
        klines = client.get_historical_klines('BTCUSDT', '5m', item['timestamp'].strftime("%d %b, %Y"), "5 min ago UTC")
        print(klines)
        computed_data = compute_data(klines)
        current_rsi = item['rsi']
        ratio_value = item['middleband'] / item['lowerband']
        if ratio_value >= ratio:
            if item['rsi'] > 30:
                return True

    return False


def stoploss_scalping_5m_rsi_bollinger(candle_close_entry, signal_candle_close, stop_loss, item=None) -> bool:
    if candle_close_entry < signal_candle_close * stop_loss:
        return True
    return False


def takeprofit_scalping_5m_rsi_bollinger(candle_close_entry, signal_candle_close, take_profit, item=None,
                                         isbot=False) -> bool:
    if isbot:
        middleband_flag = item['bbands']['valueMiddleBand'] * 1.013
        if candle_close_entry >= middleband_flag or item['candle']['close'] > signal_candle_close * take_profit:
            return True
    else:
        middleband_flag = item['middleband'] * 1.013
        if candle_close_entry >= middleband_flag or item['close'] > signal_candle_close * take_profit:
            return True
    return False
