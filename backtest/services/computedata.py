import numpy as np
from datetime import datetime
import talib as ta


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

    ema1 = ta.EMA(close_array, timeperiod=1)
    ema2 = ta.EMA(close_array, timeperiod=2)
    ema3 = ta.EMA(close_array, timeperiod=3)
    ema4 = ta.EMA(close_array, timeperiod=4)
    ema5 = ta.EMA(close_array, timeperiod=5)
    ema6 = ta.EMA(close_array, timeperiod=6)
    ema7 = ta.EMA(close_array, timeperiod=7)
    ema8 = ta.EMA(close_array, timeperiod=8)
    ema9 = ta.EMA(close_array, timeperiod=9)
    ema10 = ta.EMA(close_array, timeperiod=10)
    ema11 = ta.EMA(close_array, timeperiod=11)
    ema12 = ta.EMA(close_array, timeperiod=12)
    ema13 = ta.EMA(close_array, timeperiod=13)
    ema14 = ta.EMA(close_array, timeperiod=14)
    ema15 = ta.EMA(close_array, timeperiod=15)
    ema16 = ta.EMA(close_array, timeperiod=16)
    ema17 = ta.EMA(close_array, timeperiod=17)
    ema18 = ta.EMA(close_array, timeperiod=18)
    ema19 = ta.EMA(close_array, timeperiod=19)
    ema20 = ta.EMA(close_array, timeperiod=20)
    ema21 = ta.EMA(close_array, timeperiod=21)
    ema22 = ta.EMA(close_array, timeperiod=22)
    ema23 = ta.EMA(close_array, timeperiod=23)
    ema24 = ta.EMA(close_array, timeperiod=24)
    ema25 = ta.EMA(close_array, timeperiod=25)
    ema26 = ta.EMA(close_array, timeperiod=26)
    ema27 = ta.EMA(close_array, timeperiod=27)
    ema28 = ta.EMA(close_array, timeperiod=28)
    ema29 = ta.EMA(close_array, timeperiod=29)
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
    upperband, middleband, lowerband = ta.BBANDS(close_array, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
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
            'unix': time[i],
            'timestamp': datetime.fromtimestamp(time[i]),
            'open': open[i],
            'high': high[i],
            'low': low[i],
            'close': close[i],
            'volume': volume[i],
            'ema1': ema1[i],
            'ema2': ema2[i],
            'ema3': ema3[i],
            'ema4': ema4[i],
            'ema5': ema5[i],
            'ema6': ema6[i],
            'ema7': ema7[i],
            'ema8': ema8[i],
            'ema9': ema9[i],
            'ema10': ema10[i],
            'ema11': ema11[i],
            'ema12': ema12[i],
            'ema13': ema13[i],
            'ema14': ema14[i],
            'ema15': ema15[i],
            'ema16': ema16[i],
            'ema17': ema17[i],
            'ema18': ema18[i],
            'ema19': ema19[i],
            'ema20': ema20[i],
            'ema21': ema21[i],
            'ema22': ema22[i],
            'ema23': ema23[i],
            'ema24': ema24[i],
            'ema25': ema25[i],
            'ema26': ema26[i],
            'ema27': ema27[i],
            'ema28': ema28[i],
            'ema29': ema29[i],
            'ema30': ema30[i],
            'ema34': ema34[i],
            'ema42': ema42[i],
            'ema50': ema50[i],
            'ema55': ema55[i],
            'ema60': ema60[i],
            'ema100': ema100[i],
            'ema189': ema189[i],
            'ema200': ema200[i],
            'ema223': ema223[i],
            'ema288': ema288[i],
            'ema365': ema365[i],
            'rsi': rsi[i],
            'macd': macd[i],
            'madsignal': macdsignal[i],
            'macdhist': macdhist[i],
            'atr': atr[i],
            'trix': trix[i],
            'slowk': slowk[i],
            'slowd': slowd[i],
            'fastk': fastk[i],
            'fastd': fastd[i],
            'fastk_rsi': fastk_rsi[i],
            'fastd_rsi': fastd_rsi[i],
            'upperband': upperband[i],
            'middleband': middleband[i],
            'lowerband': lowerband[i],
            'ma20': ma20[i],
            'ma20_rsi': ma20_rsi[i],
            'doji': doji[i],
            'white_soldier': white_soldier[i],
            'hammer': hammer[i],
            'adx': adx[i]
        }

        computed_data.append(diz)

    return computed_data
