from time import sleep

import decouple
import json
import redis
from binance import Client
import talib
import numpy as np

from strategy.models import SymbolExchange


class RealTimeIndicator:
    close_array = None
    open_array = None
    low_array = None
    high_array = None

    def __init__(self, symbol, time_frame, realtime):
        self.symbol = symbol
        self.time_frame = time_frame
        self.redis = True
        self.realtime = realtime
        self.client = Client()
        self.redis_client = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)

    def compute(self, start_time=None):

        klines = None

        """
        [
          [
            1499040000000,      // Open time
            "0.01634790",       // Open
            "0.80000000",       // High
            "0.01575800",       // Low
            "0.01577100",       // Close
            "148976.11427815",  // Volume
            1499644799999,      // Close time
            "2434.19055334",    // Quote asset volume
            308,                // Number of trades
            "1756.87402397",    // Taker buy base asset volume
            "28.46694368",      // Taker buy quote asset volume
            "17928899.62484339" // Ignore.
          ]
        ]
        """

        if self.redis is False:
            try:
                if start_time is not None:
                    klines = self.client.get_klines(symbol=self.symbol, interval=self.time_frame, endTime=start_time)
                if start_time is None:
                    klines = self.client.get_klines(symbol=self.symbol, interval=self.time_frame)

            except Exception as e:
                print("Binance Error:" + str(e))
                sleep(30)
                if start_time is not None:
                    klines = self.client.get_klines(symbol=self.symbol, interval=self.time_frame, endTime=start_time)
                if start_time is None:
                    klines = self.client.get_klines(symbol=self.symbol, interval=self.time_frame)

            open_time = [entry[0] for entry in klines]
            open = [float(entry[1]) for entry in klines]
            high = [float(entry[2]) for entry in klines]
            low = [float(entry[3]) for entry in klines]
            close = [float(entry[4]) for entry in klines]
            close_time = [entry[6] for entry in klines]

            self.close_array = np.asarray(close)
            self.open_array = np.asarray(open)
            self.low_array = np.asarray(low)
            self.high_array = np.asarray(high)

        else:
            if self.realtime:
                key = str(SymbolExchange.objects.get(symbol=self.symbol)) + "_" + str(self.time_frame) + "_REALTIME"
                if self.redis_client.exists(key):
                    """
                     candle_realtime = {
    
                                        'candle_close': close_price,
                                        'candle_open': open_price,
                                        'candle_high': high_price,
                                        'candle_low': low_price,
                                        'is_closed': is_closed,
                                        'time_milliseconds': kline_start_time,
                                        # 'time_datetime': datetime.datetime.fromtimestamp(kline['kline_start_time'] / 1000.0,tz=datetime.timezone.utc),
                                    }
                    """

                    klines = json.loads(self.redis_client.get(key))
                    open = [float(entry['candle_open']) for entry in klines]
                    high = [float(entry['candle_high']) for entry in klines]
                    low = [float(entry['candle_low']) for entry in klines]
                    close = [float(entry['candle_close']) for entry in klines if entry['is_closed']]

                    self.close_array = np.asarray(close)
                    self.open_array = np.asarray(open)
                    self.low_array = np.asarray(low)
                    self.high_array = np.asarray(high)
            else:

                key = str(SymbolExchange.objects.get(symbol=self.symbol)) + "_" + str(self.time_frame) + "_CLOSED"
                if self.redis_client.exists(key):
                    """
                     candle_realtime = {

                                        'candle_close': close_price,
                                        'candle_open': open_price,
                                        'candle_high': high_price,
                                        'candle_low': low_price,
                                        'is_closed': is_closed,
                                        'time_milliseconds': kline_start_time,
                                        # 'time_datetime': datetime.datetime.fromtimestamp(kline['kline_start_time'] / 1000.0,tz=datetime.timezone.utc),
                                    }
                    """

                    klines = json.loads(self.redis_client.get(key))
                    print(len(klines))
                    open = [float(entry['candle_open']) for entry in klines]
                    high = [float(entry['candle_high']) for entry in klines]
                    low = [float(entry['candle_low']) for entry in klines]
                    close = [float(entry['candle_close']) for entry in klines]

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
