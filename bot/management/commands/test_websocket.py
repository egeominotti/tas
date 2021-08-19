import numpy
import numpy as np
import talib
from django.core.management import BaseCommand
import logging

logger = logging.getLogger('main')
from bot.models import BufferRecordData


class Command(BaseCommand):
    help = 'Test '

    def handle(self, *args, **kwargs):

        close = []
        open = []
        low = []
        high = []

        for k in BufferRecordData.objects.filter(key='BTCUSDT_5m'):
            close.append(k.close_candle)
            open.append(k.open_candle)
            low.append(k.low_candle)
            high.append(k.high_candle)

        close_array = np.asarray(close)
        open_array = np.asarray(open)
        low_array = np.asarray(low)
        high_array = np.asarray(high)

        ema5 = talib.EMA(close_array, timeperiod=5)
        ema7 = talib.EMA(close_array, timeperiod=7)
        ema8 = talib.EMA(close_array, timeperiod=8)
        ema9 = talib.EMA(close_array, timeperiod=9)
        ema10 = talib.EMA(close_array, timeperiod=10)
        ema12 = talib.EMA(close_array, timeperiod=12)
        ema13 = talib.EMA(close_array, timeperiod=13)
        ema21 = talib.EMA(close_array, timeperiod=21)
        ema24 = talib.EMA(close_array, timeperiod=24)
        ema30 = talib.EMA(close_array, timeperiod=30)
        ema34 = talib.EMA(close_array, timeperiod=34)
        ema42 = talib.EMA(close_array, timeperiod=42)
        ema50 = talib.EMA(close_array, timeperiod=50)
        ema55 = talib.EMA(close_array, timeperiod=55)
        ema60 = talib.EMA(close_array, timeperiod=60)
        ema100 = talib.EMA(close_array, timeperiod=100)
        ema189 = talib.EMA(close_array, timeperiod=189)
        ema200 = talib.EMA(close_array, timeperiod=200)
        ema223 = talib.EMA(close_array, timeperiod=223)
        ema288 = talib.EMA(close_array, timeperiod=288)
        ema365 = talib.EMA(close_array, timeperiod=365)

        rsi = talib.RSI(close_array, timeperiod=14)
        macd, macdsignal, macdhist = talib.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)
        atr = talib.ATR(high_array, low_array, close_array, timeperiod=14)
        trix = talib.TRIX(close_array, timeperiod=30)
        slowk, slowd = talib.STOCH(high_array, low_array, close_array, fastk_period=5, slowk_period=3, slowk_matype=0,
                                slowd_period=3, slowd_matype=0)
        fastk, fastd = talib.STOCHF(high_array, low_array, close_array, fastk_period=5, fastd_period=3, fastd_matype=0)
        fastk_rsi, fastd_rsi = talib.STOCHRSI(close_array, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        upperband, middleband, lowerband = talib.BBANDS(close_array, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        ma20 = talib.MA(close_array, timeperiod=20, matype=0)
        ma20_rsi = talib.MA(rsi, timeperiod=20, matype=0)
        doji = talib.CDLDOJI(open_array, high_array, low_array, close_array)
        white_soldier = talib.CDL3WHITESOLDIERS(open_array, high_array, low_array, close_array)
        hammer = talib.CDLHAMMER(open_array, high_array, low_array, close_array)
        adx = talib.ADX(high_array, low_array, close_array, timeperiod=14)

        print(upperband[-1])
        print(middleband[-1])
        print(lowerband[-1])
        print(round(rsi[-2],2))
        print(ema7[-1])
        print(ema5[-1])
        print(ema9[-1])
