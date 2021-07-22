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

    def rsi(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'rsi?' + self.base + "&interval=" + str(interval)).content)

    def macd(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'macd?' + self.base + "&interval=" + str(interval)).content)

    def bollinger(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'bbands?' + self.base + "&interval=" + str(interval)).content)

    def fibonacciretracement(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'fibonacciretracement?' + self.base + "&interval=" + str(interval)).content)

    def candle(self, interval):
        return json.loads(
            requests.get(
                self.BASE_URL + 'candle?' + self.base + "&interval=" + str(interval)).content)

    def candles(self, interval, period):
        return json.loads(
            requests.get(
                self.BASE_URL + 'candles?' + self.base + "&interval=" + str(interval) + "&period=" + str(
                    period)).content)
