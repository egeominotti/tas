from bot.services.telegram import Telegram
from time import sleep
import datetime
import signal

"""
Logic function
"""
from exchange.model.binance import BinanceHelper

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
        self.notify = True
        self.live = True
        self.exchange = BinanceHelper(
            symbol=self.symbol_exchange,
            leverage=2
        )

        type = None
        if self.func_exit.short and self.func_entry.short:
            type = 'SHORT'
        if self.func_exit.long and self.func_exit.long:
            type = 'LONG'

        self.item = {
            'candle_close': 0,
            'entry_candle': 0,
            'takeprofit_ratio': 0,
            'takeprofit_candle': 0,
            'takeprofit': False,
            'stoploss_ratio': 0,
            'stoploss_candle': 0,
            'stoploss': False,
            'entry': False,
            'sleep_func_entry': self.func_entry.sleep,
            'sleep_func_exit': self.func_exit.sleep,
            'taapi': self.taapi,
            'symbol': self.symbol,
            'symbol_exchange': self.symbol_exchange,
            'type': type,
            'time_frame': self.time_frame,
            'ratio': self.func_entry.ratio,
            'stoploss_value': self.func_exit.stop_loss,
            'takeprofit_value': self.func_exit.take_profit,
            'entry_function': False,
            'exit_function': False
        }

    def start(self) -> None:

        if self.notify:
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            start = "Started: " + str(self.current_bot.name) + \
                    "\n" + "Balance: " + str(self.exchange.get_current_balance_futures_('USDT')) + \
                    "\n" + "Quantity of investement: " + str(self.exchange.quantity) + \
                    "\n" + "Symbol: " + str(self.symbol) + \
                    "\nTime frame: " + str(self.time_frame) + \
                    "\nStarted at: " + str(now) + \
                    "\nLet's go to the moon 🚀️"
            self.telegram.send(start)

    def entry(self) -> bool:

        func_entry = eval(self.func_entry.name)
        if self.item.get('entry') is False:

            func_entry(item=self.item, bot=True)
            if self.item.get('entry') is True:

                self.item['entry_function'] = True
                self.item['takeprofit_ratio'] = self.item.get('entry_candle') * self.item.get('takeprofit_value')
                self.item['stoploss_ratio'] = self.item.get('entry_candle') * self.item.get('stoploss_value')

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    entry_text = "Bot: " + str(self.current_bot.name) + \
                                 "\n" + "Symbol: " + str(self.symbol) + \
                                 "\nTime frame: " + str(self.time_frame) + \
                                 "\nEntry Candle value: " + str(self.item.get('entry_candle')) + \
                                 "\nEntry Candle date: " + str(now)
                    self.telegram.send(entry_text)

                if self.live:
                    self.exchange.buy_market()

                self.item['takeprofit_ratio'] = self.item.get('entry_candle') * self.item.get('takeprofit_value')
                self.item['stoploss_ratio'] = self.item.get('entry_candle') * self.item.get('stoploss_value')

                return True

            print(self.item)
            # Wait sleep_func_entry seconds
            sleep(self.item.get('sleep_func_entry'))

    def exit(self) -> bool:

        func_exit = eval(self.func_exit.name)
        if self.item.get('entry') is True:

            func_exit(item=self.item, bot=True)

            """
            Stoploss
            """
            if self.item.get('stoploss'):

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    stop_loss = "Bot: " + str(self.current_bot.name) + \
                                "\n" + "Symbol: " + str(self.symbol) + \
                                "\nTime frame: " + str(self.time_frame) + \
                                "\nStoploss candle value: " + str(self.item.get('stoploss_candle')) + \
                                "\nStoploss candle date: " + str(now)
                    self.telegram.send(stop_loss)

                if self.live:
                    self.exchange.sell_market()

                return True

            """
            Takeprofit
            """
            if self.item.get('takeprofit'):

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    stop_loss = "Bot: " + str(self.current_bot.name) + \
                                "\n" + "Symbol: " + str(self.symbol) + \
                                "\nTime frame: " + str(self.time_frame) + \
                                "\nTakeprofit candle value: " + str(self.item.get('takeprofit_candle')) + \
                                "\nTakeprofit candle date: " + str(now)
                    self.telegram.send(stop_loss)

                if self.live:
                    self.exchange.sell_market()

                return True

            print(self.item)

    def run(self) -> bool:

        self.start()

        entry = False
        while True:

            try:

                if entry is False:

                    if self.entry():
                        # Succesful open position
                        entry = True

                if entry is True:
                    self.item['exit_function'] = True
                    if self.exit():
                        # Successful close position in takeprofit or stoploss
                        break

            except Exception as e:
                exception = "ERROR" + str(e)
                self.telegram.send(exception)
                return False

        return True
