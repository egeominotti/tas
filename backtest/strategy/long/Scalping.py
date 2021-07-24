import datetime
from analytics.services.exchangeApi import Taapi

"""
Classe per astrarre i test passando i valori dai file oppure dal db
"""


class ScalpingTest:

    TAKE_PROFIT = 1.01
    STOP_LOSS = 0.95
    RATIO = 1.0005

    taapi = None
    candle_value = None
    ema1 = None
    ema2 = None
    sentinel = False
    value = None
    type = None

    def settypestrategy(self, type):
        self.type = type

    def gettypestrategy(self):
        return self.type

    def setema(self, ema1, ema2):
        self.ema1 = ema1
        self.ema2 = ema2

    def setvaluecandle(self, candle_value):
        self.candle_value = candle_value

    def getvaluecandle(self):
        return self.candle_value

    def setratio(self, ratio):
        self.RATIO = ratio

    def getratio(self):
        return self.RATIO

    def settakeprofit(self, takeprofit):
        self.TAKE_PROFIT = takeprofit

    def setstoploss(self, stoploss):
        self.STOP_LOSS = stoploss

    def strategy(self):

        candle_close = self.getvaluecandle()

        if self.sentinel is False:

            """
            STRATEGY: LONG
            """
            if self.gettypestrategy() == 'LONG':
                if self.ema1 >= self.ema2:
                    if candle_close > self.ema1:
                        ratio_value = self.ema1 / self.ema2
                        if ratio_value < self.RATIO:
                            print("---------------------------------------------------")
                            print("Compro LONG al prezzo: " + str(candle_close))
                            print("TP:" + str(candle_close * self.TAKE_PROFIT))
                            print("SL:" + str(candle_close * self.STOP_LOSS))
                            print("---------------------------------------------------")

                            self.value = candle_close
                            self.sentinel = True
            """
            STRATEGY: LONG
            """
            if self.gettypestrategy() == 'SHORT':
                if self.ema1 <= self.ema2:
                    if candle_close < self.ema1:
                        ratio_value = self.ema2 / self.ema1
                        if ratio_value < self.RATIO:
                            print("---------------------------------------------------")
                            print("Compro LONG al prezzo: " + str(candle_close))
                            print("TP:" + str(candle_close * self.TAKE_PROFIT))
                            print("SL:" + str(candle_close * self.STOP_LOSS))
                            print("---------------------------------------------------")

                            self.value = candle_close
                            self.sentinel = True

        if self.sentinel is True:

            if self.gettypestrategy() == 'LONG':

                """
                TAKE PROFIT
                """
                if candle_close > self.value * self.TAKE_PROFIT:
                    print("Chiusura posizione long: " + str(self.value * self.TAKE_PROFIT))
                    self.sentinel = False

                """
                STOP LOSS
                """
                if candle_close < self.value * self.STOP_LOSS:
                    print("STOP LOSS")
                    self.sentinel = False

            if self.gettypestrategy() == 'SHORT':

                """
                TAKE PROFIT
                """
                if candle_close < self.value * self.TAKE_PROFIT:
                    print("Chiusura posizione long: " + str(self.value * self.TAKE_PROFIT))
                    self.sentinel = False

                """
                STOP LOSS
                """
                if candle_close > self.value * self.STOP_LOSS:
                    print("STOP LOSS")
                    self.sentinel = False


"""
Classe per l'astrazione dei test long/short utilizzando due ema e una candela : utilizzo delle api in tempo reale
"""


class Scalping:
    TAKE_PROFIT = 1.01
    STOP_LOSS = 0.95
    RATIO = 1.0005

    lsitTimeSplit = [0, 15, 30, 45]

    taapi = None
    candle_interval = None
    ema1 = None
    ema1_interval = None
    ema2 = None
    ema2_interval = None
    sentinel = None
    value = None

    def __init__(self, ticker):
        self.taapi = Taapi(ticker)

    def setema(self, ema1, ema1_interval, ema2, ema2_interval):
        self.ema1 = ema1
        self.ema1_interval = ema1_interval
        self.ema2 = ema2
        self.ema2_interval = ema2_interval

    def settimecandle(self, candle_interval):
        self.candle_interval = candle_interval

    def setratio(self, ratio):
        self.RATIO = ratio

    def settakeprofit(self, takeprofit):
        self.TAKE_PROFIT = takeprofit

    def setstoploss(self, stoploss):
        self.STOP_LOSS = stoploss

    def strategy(self):
        now = datetime.datetime.now()
        candle_close = self.taapi.candle(self.candle_interval).get('close')

        if self.sentinel is False:
            for k in self.lsitTimeSplit:
                if k == now.minute:
                    ema1 = self.taapi.ema(self.ema1, self.ema1_interval)
                    ema2 = self.taapi.ema(self.ema2, self.ema2_interval)
                    if ema1 >= ema2:
                        if candle_close > ema1:
                            ratio_value = ema1 / ema2
                            if ratio_value < self.RATIO:
                                print("---------------------------------------------------")
                                print("Compro LONG al prezzo: " + str(candle_close))
                                print("TP:" + str(candle_close * self.TAKE_PROFIT))
                                print("SL:" + str(candle_close * self.STOP_LOSS))
                                print("---------------------------------------------------")

                                self.value = candle_close
                                self.sentinel = True

        if self.sentinel is True:

            """
            Take profit short
            """
            if candle_close > self.value * self.TAKE_PROFIT:
                print("Chiusura posizione long: " + str(self.value * self.TAKE_PROFIT))
                self.sentinel = False

            """
            Stop loss 
            """
            if candle_close < self.value * self.STOP_LOSS:
                print("STOP LOSS")
                self.sentinel = False
