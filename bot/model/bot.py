from time import sleep

from binance import Client
from decouple import config

from analytics.services.exchangeApi import Taapi


class Bot:

    def __init__(
            self,
            symbol,
            time_frame,
            ratio,
            stop_loss,
            take_profit,
            func_entry,
            func_stop_loss,
            func_take_profit,
            indicator,
            ema_interval=None,
    ):
        # client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))
        # client.futures_change_leverage(symbol='BTCUSDT', marginType='ISOLATED', leverage=1)
        self.taapi = Taapi(symbol)
        self.time_frame = time_frame
        self.ratio = ratio
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.func_entry = func_entry
        self.func_stop_loss = func_stop_loss
        self.func_take_profit = func_take_profit
        self.indicator = indicator
        self.ema_interval = ema_interval

    def run(self, sleep_time=0):
        while True:

            sleep(sleep_time)

            dizIndicator = {}
            for i in self.indicator:
                print(i)
                if i == 'ema':
                    if len(self.ema_interval) > 0:
                        for e in self.ema_interval:
                            dizIndicator[i + "_" + str(e)] = getattr(self.taapi, i)(e, self.time_frame)
                else:
                    dizIndicator[i] = getattr(self.taapi, i)(self.time_frame)
            print(dizIndicator)

            if self.func_entry(dizIndicator, self.ratio, True):
                print("entro")

        # while True:
        #
        #     if sleep_time > 0:
        #         sleep(sleep_time)
        #
        #     if self.func_entry(item, self.ratio):
        #
        #         while True:
        #             self.stop_loss()
        #             self.take_profit()

    def stop_loss(self, sleep_time=0):
        self.func_stop_loss()

    def take_profit(self, sleep_time=0):
        self.func_take_profit()
