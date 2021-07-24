import datetime
from analytics.services.exchangeApi import Taapi


class Scalping:
    interval = 0
    QUANTITY = 0.004
    TAKE_PROFIT = 1.01
    STOP_LOSS = 0.95
    lsitTimeSplit = [
        0, 15, 30, 45
    ]

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
                            ratio = ema1 / ema2
                            if ratio < 1.0005:

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
