import requests
import json


class Taapi:
    symbol = None
    BASE = None
    EXCHANGE = 'binance'
    BASE_URL = 'https://api.taapi.io/'
    API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBpZXJyaTkzQGdtYWlsLmNvbSIsImlhdCI6MTYyNzAzNTMzNSwiZXhwIjo3OTM0MjM1MzM1fQ.m1f7RuvDmmdrTd1l8W7SSd_DVZxn9eabEjCoE8zED-Y'

    def __init__(self, symbol, api_extra=None):
        self.symbol = symbol
        self.base = 'secret=' + self.API_KEY + "&exchange=" + self.EXCHANGE + "&symbol=" + self.symbol
        if api_extra is not None:
            self.base = 'secret=' + api_extra + "&exchange=" + self.EXCHANGE + "&symbol=" + self.symbol

    # https://taapi.io/indicators/exponential-moving-average/
    def ema(self, ema, interval, backtrack=None, backtracks=None):
        """
        {
          "timestampHuman": "2021-01-14 15:00:00 (Thursday) UTC",
          "timestamp": 1610636400,
          "open": 39577.53,
          "high": 39666,
          "low": 39294.7,
          "close": 39607.09,
          "volume": 1211.2841909999893
        }
        """
        if backtracks is not None:
            """
            The backtracks parameter returns the candle value calculated on every candle for the past X candles. 
            For example, if you want to know what the candle was every hour for the past 12 hours, you use backtracks=12.
             As a result, you will get 12 values back.
            """
            return json.loads(
                requests.get(
                    self.BASE_URL + 'ema?' + self.base + "&interval=" + str(interval) + "&optInTimePeriod=" + str(
                        ema) + "&backtracks=" + str(backtracks)).content)
        elif backtrack is not None:
            """
            Permette di prendere valori precedenti: Esempio (interval=1h) se imposto (backtrack=1)
            ritornerà l'ema di un'ora fa.
            
            The backtrack parameter removes candles from the data set and calculates the candle value X amount of candles back. 
            So, if you’re fetching the candle on the hourly and you want to know what the candle was 5 hours ago, set backtrack=5.
             The default is 0 and a maximum is 50. 
            """
            return json.loads(
                requests.get(
                    self.BASE_URL + 'ema?' + self.base + "&interval=" + str(interval) + "&optInTimePeriod=" + str(
                        ema) + "&backtrack=" + str(backtracks)).content)
        else:
            return json.loads(
                requests.get(
                    self.BASE_URL + 'ema?' + self.base + "&interval=" + str(interval) + "&optInTimePeriod=" + str(
                        ema)).content).get('value')

    # https://taapi.io/indicators/relative-strength-index-rsi/
    def rsi(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'rsi?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/macd/
    def macd(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'macd?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/bollinger-bands/
    def bbands(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'bbands?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/stochastic-relative-strength-index/
    def stochrsi(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'stochrsi?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/stochastic/
    def stoch(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'stoch?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/average-true-range/
    def atr(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'atr?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/fibonacci-retracement/
    def fibonacciretracement(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'fibonacciretracement?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/pivot-points/
    def pivotpoints(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'pivotpoints?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/annualized-historical-volatility/
    def volatility(self, interval, period):
        return json.loads(
            requests.get(
                self.BASE_URL + 'volatility?' + self.base + "&interval=" + str(interval) + "&period=" + str(
                    period)).content)

    # https://taapi.io/indicators/commodity-channel-index/
    def cci(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'cci?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/trix/
    def trix(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'trix?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/moving-average/
    def ma(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'ma?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/breakaway/
    def breakaway(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'breakaway?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/doji/
    def doji(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'doji?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/hammer/
    def hammer(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'hammer?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/candle/
    def candle(self, interval, backtrack=None, backtracks=None):

        if backtrack is not None:
            """
              {
                "timestampHuman": "2021-01-14 15:00:00 (Thursday) UTC",
                "timestamp": 1610636400,
                "open": 39577.53,
                "high": 39666,
                "low": 39294.7,
                "close": 39605.45,
                "volume": 1218.1425259999887,
                "backtrack": 0
              },
            """
            return json.loads(
                requests.get(
                    self.BASE_URL + 'candle?' + self.base + "&interval=" + str(interval) + "&backtack=" + str(
                        backtrack)).content)
        elif backtracks is not None:
            return json.loads(
                requests.get(
                    self.BASE_URL + 'candle?' + self.base + "&interval=" + str(interval) + "&backtacks=" + str(
                        backtrack)).content)
        else:
            return json.loads(
                requests.get(
                    self.BASE_URL + 'candle?' + self.base + "&interval=" + str(interval)).content)

    # https://taapi.io/indicators/candles/
    def candles(self, interval, period):
        return json.loads(
            requests.get(
                self.BASE_URL + 'candles?' + self.base + "&interval=" + str(interval) + "&period=" + str(
                    period)).content)
