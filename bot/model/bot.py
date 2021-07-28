from time import sleep

from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
from bot.services.binance import BinanceHelper


class TradinBot:

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
        self.telegram = Telegram()
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
        self.binance = None

        print(self.func_entry)

    def setexchange(self, symbol, quantity, leverage):
        self.binance = BinanceHelper(symbol=symbol, quantity=quantity, leverage=leverage)

    def run(self, sleep_time_position=0, sleep_time_profit_or_loss=0):

        start = "BOT started: into while contidion"
        self.telegram.send(start)

        open_position_value = 0
        position = False

        while True:

            dizIndicator = {}
            for i in self.indicator:
                if i == 'ema':
                    if len(self.ema_interval) > 0:
                        for e in self.ema_interval:
                            dizIndicator[i + "_" + str(e)] = getattr(self.taapi, i)(e, self.time_frame)
                else:
                    dizIndicator[i] = getattr(self.taapi, i)(self.time_frame)

            if position is False:
                start = "BOT started: into while contidion"
                self.telegram.send(start)

                if self.func_entry(dizIndicator, self.ratio, isbot=True):
                    open_position_value = dizIndicator['candle']['close']
                sleep(sleep_time_position)

            if position is True:

                candle_close_value = getattr(self.taapi, 'candle')(self.time_frame)['candle']['close']

                value = self.func_stop_loss(open_position_value, candle_close_value, self.stop_loss)
                if value is True:
                    print("TAKE_PROFIT: " + str(open_position_value * self.take_profit))
                    position = False

                value = self.func_take_profit(open_position_value, candle_close_value, self.take_profit, isbot=True)
                if value is True:
                    print("STOP LOSS: " + str(open_position_value * self.stop_loss))
                    position = False

                sleep(sleep_time_profit_or_loss)
