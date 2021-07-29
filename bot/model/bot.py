from time import sleep

from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
from bot.services.binance import BinanceHelper


class TradingBot:

    def __init__(
            self,
            symbol,
            symbol_exchange,
            time_frame,
            ratio,
            stop_loss,
            leverage,
            quantity_investement,
            take_profit,
            func_entry,
            func_stop_loss,
            func_take_profit,
            binance
    ):
        self.telegram = Telegram()
        self.symbol = symbol
        self.symbol_exchange = symbol_exchange
        self.taapi = Taapi(symbol)
        self.time_frame = time_frame
        self.ratio = ratio
        self.stop_loss = stop_loss
        self.leverage = leverage
        self.quantity_investement = quantity_investement
        self.take_profit = take_profit
        self.func_entry = func_entry
        self.func_stop_loss = func_stop_loss
        self.func_take_profit = func_take_profit
        self.binance = BinanceHelper(
            api_key=binance.api_key,
            api_secret=binance.api_secret,
            symbol=symbol_exchange,
            quantity=quantity_investement,
            leverage=leverage
        )

    def run(self, sleep_time_position=0, sleep_time_profit_or_loss=0):

        data = {
            'symbol': self.symbol,
            'time_frame': self.time_frame
        }

        start = "BOT started: into while contidion"
        self.telegram.send(start)

        open_position_value = 0
        position = False

        while True:
            if position is False:

                start = "BOT started: into while contidion"
                self.telegram.send(start)

                func_entry_value = self.func_entry(item=data, bot=True)
                if func_entry_value is not False:
                    open_position_value = func_entry_value
                sleep(sleep_time_position)

            if position is True:

                item = {
                    'stop_loss': self.stop_loss,
                    'take_profit': self.take_profit,
                    'open_position_value': open_position_value
                }

                value = self.func_stop_loss(item=item, bot=True)
                if value is True:
                    print("TAKE_PROFIT: " + str(open_position_value * self.take_profit))
                    position = False

                value = self.func_take_profit(item=item, bot=True)
                if value is True:
                    print("STOP LOSS: " + str(open_position_value * self.stop_loss))
                    position = False

                sleep(sleep_time_profit_or_loss)
