import datetime
from analytics.services.exchangeApi import Taapi
import abc

"""
Classe per astrarre i test passando i valori dai file oppure dal db
"""


class StrategyTest:
    TAKE_PROFIT = 1.01
    STOP_LOSS = 0.95
    RATIO = 1.0005

    taapi = None
    candle_value = None
    sentinel = False
    value = None
    type = None
    time = None
    ema1 = None
    ema2 = None
    ema3 = None
    ema4 = None

    def settypestrategy(self, type):
        self.type = type

    def gettypestrategy(self):
        return self.type

    def setema(self, ema1=None, ema2=None, ema3=None, ema4=None):
        self.ema1 = ema1
        self.ema2 = ema2
        self.ema3 = ema3
        self.ema4 = ema4

    def setvaluecandle(self, candle_value):
        self.candle_value = candle_value

    def getvaluecandle(self):
        return self.candle_value

    def settime(self, time):
        self.time = time

    def setratio(self, ratio):
        self.RATIO = ratio

    def getratio(self):
        return self.RATIO

    def settakeprofit(self, takeprofit):
        self.TAKE_PROFIT = takeprofit

    def setstoploss(self, stoploss):
        self.STOP_LOSS = stoploss

    def check_entry(self):

        candle_close = self.getvaluecandle()

        if self.gettypestrategy() == 'LONG':
            ratio_value = self.ema1 / self.ema2
            if 1 < ratio_value < self.getratio():
                if candle_close > self.ema3:
                    return candle_close

        if self.gettypestrategy() == 'SHORT':
            ratio_value = self.ema2 / self.ema1
            if 1 < ratio_value < self.getratio():
                if candle_close > self.ema3:
                    return candle_close

        return None

    def stop_loss(self, entry_candle_close_value, candle_close_iterate):
        if self.gettypestrategy() == 'LONG':
            if entry_candle_close_value < candle_close_iterate * self.STOP_LOSS:
                return True

        if self.gettypestrategy() == 'SHORT':
            if entry_candle_close_value > candle_close_iterate * self.STOP_LOSS:
                return True
        return False

    def take_profit(self, entry_candle_close_value, candle_close_iterate):

        if self.gettypestrategy() == 'LONG':
            if entry_candle_close_value > candle_close_iterate * self.TAKE_PROFIT:
                return True

        if self.gettypestrategy() == 'SHORT':
            if entry_candle_close_value < candle_close_iterate * self.TAKE_PROFIT:
                return True
        return False
