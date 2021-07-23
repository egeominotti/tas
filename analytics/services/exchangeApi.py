import requests
import json


class Taapi:
    symbol = None
    BASE = None
    EXCHANGE = 'binance'
    BASE_URL = 'https://api.taapi.io/'
    API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVnZW9taW5vdHRpQGdtYWlsLmNvbSIsImlhdCI6MTYyNjgwNjc0NSwiZXhwIjo3OTM0MDA2NzQ1fQ.27kEuy9Cih52IIq7r7nIdNYUYFVO2ClfN5bhn_0KCYU'

    def __init__(self, symbol):
        self.symbol = symbol
        self.base = 'secret=' + self.API_KEY + "&exchange=" + self.EXCHANGE + "&symbol=" + self.symbol

    # https://taapi.io/indicators/exponential-moving-average/
    def ema(self, ema, interval, backtracks=None):
        if backtracks is not None:
            return json.loads(
                requests.get(
                    self.BASE_URL + 'ema?' + self.base + "&interval=" + str(interval) + "&optInTimePeriod=" + str(
                        ema) + "&backtracks=" + str(backtracks)).content)
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
    def volatility(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'volatility?' + self.base + "&interval=" + str(interval)).content)

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

    def candle(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'candle?' + self.base + "&interval=" + str(interval)).content)

    def candles(self, interval, period):
        return json.loads(
            requests.get(
                self.BASE_URL + 'candles?' + self.base + "&interval=" + str(interval) + "&period=" + str(
                    period)).content)
