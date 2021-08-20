import talib
import numpy as np
from bot.models import BufferRecordData


class Indicator:

    def __init__(self, symbol, time_frame):
        self.symbol = symbol
        self.time_frame = time_frame

    def get_np_close_array(self, type):
        """
        :param type: close,open,high,low
        :return:
        """
        close = []
        open = []
        low = []
        high = []

        for k in BufferRecordData.objects.filter(key=self.symbol + "_" + self.time_frame):
            if type == 'close':
                close.append(k.close_candle)
            if type == 'open':
                open.append(k.open_candle)
            if type == 'low':
                low.append(k.low_candle)
            if type == 'high':
                high.append(k.high_candle)

        if type == 'close':
            return np.asarray(close)
        if type == 'open':
            return np.asarray(open)
        if type == 'low':
            return np.asarray(low)
        if type == 'high':
            return np.asarray(high)

    def ema(self, period, backtrack=-1):

        ema = talib.EMA(self.get_np_close_array('close'), timeperiod=period)
        return ema[backtrack]

    def rsi(self, period, backtrack=-1):

        rsi = talib.RSI(self.get_np_close_array('close'), timeperiod=period)
        return round(rsi[backtrack], 4)

    def bbands(self, period=20, backtrack=-1):

        upperband, middleband, lowerband = talib.BBANDS(
            self.get_np_close_array('close'),
            timeperiod=period,
            nbdevup=2,
            nbdevdn=2,
            matype=0)

        val = {
            'valueUpperBand': upperband[backtrack],
            'valueMiddleBand': middleband[backtrack],
            'valueLowerBand': lowerband[backtrack]
        }

        return val
