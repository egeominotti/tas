from bot.services.telegram import Telegram

from time import sleep
import datetime
import signal

"""
Logic function
"""

from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *


def terminate_bot():
    exit(1)


signal.signal(signal.SIGINT, terminate_bot)


class TradingBot:

    def __init__(
            self,
            current_bot,
            symbol,
            symbol_exchange,
            time_frame,
            func_entry,
            func_exit,
            logger,
            bot_object
    ):
        self.current_bot = current_bot
        self.telegram = Telegram()
        self.symbol = symbol
        self.symbol_exchange = symbol_exchange
        self.taapi = Taapi(symbol)
        self.time_frame = time_frame
        self.func_entry = func_entry
        self.func_exit = func_exit
        self.logger = logger
        self.bot_object = bot_object
        self.logger_id = self.logger.objects.create(bot=self.current_bot)
        self.notify = False
        self.item = {
            'sleep_func_entry': self.func_entry.sleep,
            'sleep_func_exit': self.func_exit.sleep,
            'taapi': self.taapi,
            'symbol': self.symbol,
            'type': self.func_exit.short or self.func_exit.long,
            'time_frame': self.time_frame,
            'ratio': self.func_entry.ratio,
            'stoploss_value': self.func_exit.stop_loss,
            'takeprofit_value': self.func_exit.take_profit,
            'takeprofit': False,
            'takeprofit_candle': 0,
            'stoploss': False,
            'stoploss_candle': 0,
            'entry': False,
            'entry_candle': 0
        }

    def start(self):

        if self.notify:
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            start = "Started: " + str(self.current_bot.name) + \
                    "\n" + "Symbol: " + str(self.symbol) + \
                    "\nTime frame: " + str(self.time_frame) + \
                    "\nStarted at: " + str(now) + \
                    "\nLet's go to the moon 🚀️"
            self.telegram.send(start)

    def entry(self):

        print("entry function")
        func_entry = eval(self.func_entry.name)
        if self.item.get('entry') is False:

            func_entry(item=self.item, bot=True)

            if self.item.get('entry') is True:

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    entry_text = "Bot: " + str(self.current_bot.name) + \
                                 "\n" + "Symbol: " + str(self.symbol) + \
                                 "\nTime frame: " + str(self.time_frame) + \
                                 "\nEntry Candle value: " + str(self.item.get('entry_candle')) + \
                                 "\nEntry Candle date: " + str(now)
                    self.telegram.send(entry_text)

                return True

            print(self.item)
            # Wait sleep_func_entry seconds
            sleep(self.item.get('sleep_func_entry'))

    def exit(self):

        print("exit function")
        func_exit = eval(self.func_exit.name)
        if self.item.get('entry') is True:

            func_exit(item=self.item, bot=True)

            if self.item.get('stoploss'):

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    stop_loss = "Bot: " + str(self.current_bot.name) + \
                                "\n" + "Symbol: " + str(self.symbol) + \
                                "\nTime frame: " + str(self.time_frame) + \
                                "\nStoploss candle value: " + str(self.item.get('stoploss_candle')) + \
                                "\nStoploss candle date: " + str(now)
                    self.telegram.send(stop_loss)

                return True

            if self.item.get('takeprofit'):

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    stop_loss = "Bot: " + str(self.current_bot.name) + \
                                "\n" + "Symbol: " + str(self.symbol) + \
                                "\nTime frame: " + str(self.time_frame) + \
                                "\nTakeprofit candle value: " + str(self.item.get('takeprofit_candle')) + \
                                "\nTakeprofit candle date: " + str(now)
                    self.telegram.send(stop_loss)

                return True

            print(self.item)
            # Wait sleep_func_entry seconds
            sleep(self.item.get('sleep_func_entry'))

    def run(self):

        entry = False
        while True:

            try:

                if entry is False:

                    if self.entry():
                        # Succesful open position
                        entry = True

                if entry is True:
                    if self.exit():
                        # Successful close position in takeprofit or stoploss
                        break

            except Exception as e:
                exception = "ERROR" + str(e)
                self.telegram.send(exception)
