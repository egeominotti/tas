import datetime
from time import sleep
import talib
import numpy as np
from bot.models import BufferRecordData
from binance import Client


class RealTimeIndicator:
    close_array = None
    open_array = None
    low_array = None
    high_array = None

    def __init__(self, symbol, time_frame, api_key, api_secret):
        self.symbol = symbol
        self.time_frame = time_frame
        self.client = Client(api_key, api_secret)

    def compute(self):

        try:
            # klines = self.client.get_historical_klines(self.symbol, self.time_frame, 'now UTC', '1 day ago UTC')
            klines = self.client.get_historical_klines(self.symbol, self.time_frame, end_str='now UTC', start_str='1 day ago UTC')
        except Exception as e:
            print("Binance Error:" + str(e))
            sleep(30)
            klines = self.client.get_historical_klines(self.symbol, self.time_frame, end_str='now UTC', start_str='1 day ago UTC')

        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]

        self.close_array = np.asarray(close)
        self.open_array = np.asarray(open)
        self.low_array = np.asarray(low)
        self.high_array = np.asarray(high)

    def candle(self, backtrack=-1):

        value = {
            'close': self.close_array[backtrack],
            'open': self.open_array[backtrack],
            'low': self.low_array[backtrack],
            'high': self.high_array[backtrack]
        }

        return value

    def ema(self, period, backtrack=-1):

        if len(self.close_array) >= period:
            ema = talib.EMA(self.close_array, timeperiod=period)
            return round(ema[backtrack], 5)

        return None

    def rsi(self, period, backtrack=-1):

        if len(self.close_array) >= period:
            rsi = talib.RSI(self.close_array, timeperiod=period)
            return round(rsi[backtrack], 3)

        return None

    def bbands(self, period=20, backtrack=-1):

        if len(self.close_array) >= period:
            upperband, middleband, lowerband = talib.BBANDS(
                self.close_array,
                timeperiod=period,
                nbdevup=2,
                nbdevdn=2,
                matype=0)

            bbands = {
                'valueUpperBand': round(upperband[backtrack], 5),
                'valueMiddleBand': round(middleband[backtrack], 5),
                'valueLowerBand': round(lowerband[backtrack], 5)
            }

            return bbands

        return None


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

    def candle(self, backtrack=-1):

        close_candle = self.get_np_close_array('close')
        open_candle = self.get_np_close_array('open')
        low_candle = self.get_np_close_array('low')
        high_candle = self.get_np_close_array('high')

        value = {
            'close': close_candle[backtrack],
            'open': open_candle[backtrack],
            'low': low_candle[backtrack],
            'high': high_candle[backtrack]
        }

        return value

    def ema(self, period, backtrack=-1):

        close_array = self.get_np_close_array('close')

        if len(close_array) >= period:
            ema = talib.EMA(close_array, timeperiod=period)
            return ema[backtrack]

        return None

    def rsi(self, period, backtrack=-1):

        close_array = self.get_np_close_array('close')

        if len(close_array) >= period:
            rsi = talib.RSI(close_array, timeperiod=period)
            return rsi[backtrack]

        return None

    def bbands(self, period=20, backtrack=-1):

        close_array = self.get_np_close_array('close')

        if len(close_array) >= period:
            upperband, middleband, lowerband = talib.BBANDS(
                close_array,
                timeperiod=period,
                nbdevup=2,
                nbdevdn=2,
                matype=0)

            bbands = {
                'valueUpperBand': upperband[backtrack],
                'valueMiddleBand': middleband[backtrack],
                'valueLowerBand': lowerband[backtrack]
            }

            return bbands

        return None
