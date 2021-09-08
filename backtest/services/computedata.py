import json
import numpy as np
from datetime import datetime
import talib as ta
from numpyencoder import NumpyEncoder


def compute_data_to_store(klines):
    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]

    close_array = np.asarray(close)
    open_array = np.asarray(open)
    low_array = np.asarray(low)
    high_array = np.asarray(high)

    ema5 = ta.EMA(close_array, timeperiod=5)
    ema7 = ta.EMA(close_array, timeperiod=7)
    ema8 = ta.EMA(close_array, timeperiod=8)
    ema9 = ta.EMA(close_array, timeperiod=9)
    ema10 = ta.EMA(close_array, timeperiod=10)
    ema12 = ta.EMA(close_array, timeperiod=12)
    ema13 = ta.EMA(close_array, timeperiod=13)
    ema21 = ta.EMA(close_array, timeperiod=21)
    ema24 = ta.EMA(close_array, timeperiod=24)
    ema30 = ta.EMA(close_array, timeperiod=30)
    ema34 = ta.EMA(close_array, timeperiod=34)
    ema42 = ta.EMA(close_array, timeperiod=42)
    ema50 = ta.EMA(close_array, timeperiod=50)
    ema55 = ta.EMA(close_array, timeperiod=55)
    ema60 = ta.EMA(close_array, timeperiod=60)
    ema100 = ta.EMA(close_array, timeperiod=100)
    ema189 = ta.EMA(close_array, timeperiod=189)
    ema200 = ta.EMA(close_array, timeperiod=200)
    ema223 = ta.EMA(close_array, timeperiod=223)
    ema288 = ta.EMA(close_array, timeperiod=288)
    ema365 = ta.EMA(close_array, timeperiod=365)

    rsi = ta.RSI(close_array, timeperiod=14)
    macd, macdsignal, macdhist = ta.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)
    atr = ta.ATR(high_array, low_array, close_array, timeperiod=14)
    trix = ta.TRIX(close_array, timeperiod=30)
    slowk, slowd = ta.STOCH(high_array, low_array, close_array, fastk_period=5, slowk_period=3, slowk_matype=0,
                            slowd_period=3, slowd_matype=0)
    fastk, fastd = ta.STOCHF(high_array, low_array, close_array, fastk_period=5, fastd_period=3, fastd_matype=0)
    fastk_rsi, fastd_rsi = ta.STOCHRSI(close_array, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    upperband, middleband, lowerband = ta.BBANDS(close_array, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    ma20 = ta.MA(close_array, timeperiod=20, matype=0)
    ma20_rsi = ta.MA(rsi, timeperiod=20, matype=0)
    doji = ta.CDLDOJI(open_array, high_array, low_array, close_array)
    white_soldier = ta.CDL3WHITESOLDIERS(open_array, high_array, low_array, close_array)
    hammer = ta.CDLHAMMER(open_array, high_array, low_array, close_array)
    adx = ta.ADX(high_array, low_array, close_array, timeperiod=14)

    diz = {
        'open': float(open[-1]),
        'high': float(high[-1]),
        'low': float(low[-1]),
        'close': float(close[-1]),
        'ema5': float(ema5[-1]),
        # 'ema7': ema7[-1],
        # 'ema8': ema8[-1],
        # 'ema9': ema9[-1],
        'ema10': float(ema10[-1]),
        # 'ema12': ema12[-1],
        # 'ema13': ema13[-1],
        # 'ema21': ema21[-1],
        # 'ema24': ema24[-1],
        'ema30': float(ema30[-1]),
        # 'ema34': ema34[-1],
        # 'ema42': ema42[-1],
        'ema50': float(ema50[-1]),
        # 'ema55': ema55[-1],
        # 'ema60': ema60[-1],
        'ema100': float(ema100[-1]),
        # 'ema189': ema189[-1],
        'ema200': float(ema200[-1]),
        # 'ema223': ema223[-1],
        # 'ema288': ema288[-1],
        # 'ema365': ema365[-1],
        'rsi': round(float(rsi[-1]), 4),
        # 'macd': macd[-1],
        # 'madsignal': macdsignal[-1],
        # 'macdhist': macdhist[-1],
        # 'atr': atr[-1],
        # 'trix': trix[-1],
        # 'slowk': slowk[-1],
        # 'slowd': slowd[-1],
        # 'fastk': fastk[-1],
        # 'fastd': fastd[-1],
        # 'fastk_rsi': float(fastk_rsi[-1]),
        # 'fastd_rsi': fastd_rsi[-1],
        'upperband': round(float(upperband[-1]),4),
        'middleband': round(float(middleband[-1]),4),
        'lowerband': round(float(lowerband[-1]),4),
        # 'ma20': ma20[-1],
        # 'ma20_rsi': ma20_rsi[-1],
        # 'doji': doji[-1],
        # 'white_soldier': white_soldier[-1],
        # 'hammer': hammer[-1],
        # 'adx': adx[-1]
    }

    return json.dumps(diz)


def compute_data(klines):
    time = [entry[0] / 1000 for entry in klines]
    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]
    volume = [float(entry[5]) for entry in klines]

    close_array = np.asarray(close)
    open_array = np.asarray(open)
    low_array = np.asarray(low)
    high_array = np.asarray(high)

    ema5 = ta.EMA(close_array, timeperiod=5)
    ema7 = ta.EMA(close_array, timeperiod=7)
    ema8 = ta.EMA(close_array, timeperiod=8)
    ema9 = ta.EMA(close_array, timeperiod=9)
    ema10 = ta.EMA(close_array, timeperiod=10)
    ema12 = ta.EMA(close_array, timeperiod=12)
    ema13 = ta.EMA(close_array, timeperiod=13)
    ema21 = ta.EMA(close_array, timeperiod=21)
    ema24 = ta.EMA(close_array, timeperiod=24)
    ema30 = ta.EMA(close_array, timeperiod=30)
    ema34 = ta.EMA(close_array, timeperiod=34)
    ema42 = ta.EMA(close_array, timeperiod=42)
    ema50 = ta.EMA(close_array, timeperiod=50)
    ema55 = ta.EMA(close_array, timeperiod=55)
    ema60 = ta.EMA(close_array, timeperiod=60)
    ema100 = ta.EMA(close_array, timeperiod=100)
    ema189 = ta.EMA(close_array, timeperiod=189)
    ema200 = ta.EMA(close_array, timeperiod=200)
    ema223 = ta.EMA(close_array, timeperiod=223)
    ema288 = ta.EMA(close_array, timeperiod=288)
    ema365 = ta.EMA(close_array, timeperiod=365)

    rsi = ta.RSI(close_array, timeperiod=14)
    macd, macdsignal, macdhist = ta.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)
    atr = ta.ATR(high_array, low_array, close_array, timeperiod=14)
    trix = ta.TRIX(close_array, timeperiod=30)
    slowk, slowd = ta.STOCH(high_array, low_array, close_array, fastk_period=5, slowk_period=3, slowk_matype=0,
                            slowd_period=3, slowd_matype=0)
    fastk, fastd = ta.STOCHF(high_array, low_array, close_array, fastk_period=5, fastd_period=3, fastd_matype=0)
    fastk_rsi, fastd_rsi = ta.STOCHRSI(close_array, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    upperband, middleband, lowerband = ta.BBANDS(close_array, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    ma20 = ta.MA(close_array, timeperiod=20, matype=0)
    ma20_rsi = ta.MA(rsi, timeperiod=20, matype=0)
    doji = ta.CDLDOJI(open_array, high_array, low_array, close_array)
    white_soldier = ta.CDL3WHITESOLDIERS(open_array, high_array, low_array, close_array)
    hammer = ta.CDLHAMMER(open_array, high_array, low_array, close_array)
    adx = ta.ADX(high_array, low_array, close_array, timeperiod=14)

    computed_data = []
    lenght = len(time)

    for i in range(lenght):
        diz = {
            'unix': time[-1],
            'timestamp': datetime.fromtimestamp(time[-1]),
            'open': open[-1],
            'high': high[-1],
            'low': low[-1],
            'close': close[-1],
            'volume': volume[-1],
            'ema5': ema5[-1],
            'ema7': ema7[-1],
            'ema8': ema8[-1],
            'ema9': ema9[-1],
            'ema10': ema10[-1],
            'ema12': ema12[-1],
            'ema13': ema13[-1],
            'ema21': ema21[-1],
            'ema24': ema24[-1],
            'ema30': ema30[-1],
            'ema34': ema34[-1],
            'ema42': ema42[-1],
            'ema50': ema50[-1],
            'ema55': ema55[-1],
            'ema60': ema60[-1],
            'ema100': ema100[-1],
            'ema189': ema189[-1],
            'ema200': ema200[-1],
            'ema223': ema223[-1],
            'ema288': ema288[-1],
            'ema365': ema365[-1],
            'rsi': rsi[-1],
            'macd': macd[-1],
            'madsignal': macdsignal[-1],
            'macdhist': macdhist[-1],
            'atr': atr[-1],
            'trix': trix[-1],
            'slowk': slowk[-1],
            'slowd': slowd[-1],
            'fastk': fastk[-1],
            'fastd': fastd[-1],
            'fastk_rsi': fastk_rsi[-1],
            'fastd_rsi': fastd_rsi[-1],
            'upperband': upperband[-1],
            'middleband': middleband[-1],
            'lowerband': lowerband[-1],
            'ma20': ma20[-1],
            'ma20_rsi': ma20_rsi[-1],
            'doji': doji[-1],
            'white_soldier': white_soldier[-1],
            'hammer': hammer[-1],
            'adx': adx[-1]
        }

        computed_data.append(diz)

    return computed_data
