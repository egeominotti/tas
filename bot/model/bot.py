from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
from exchange.model.binance import BinanceHelper
from time import sleep
import datetime
import signal

"""
Logic function
"""

from backtest.strategy.logic.logic_function import *

run = True


def handler_stop_signals(signum, frame):
    global run
    print("SIGNAL DI STOP")
    # todo: devo chiudere la posizione se è aperta e cancellare il bot
    run = False


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)


class TradingBot:

    def __init__(
            self,
            current_bot,
            user,
            symbol,
            symbol_exchange,
            time_frame,
            func_entry,
            func_exit,
            logger,
            bot_object
    ):
        self.current_bot = current_bot
        self.user = user
        self.telegram = Telegram()
        self.symbol = symbol
        self.symbol_exchange = symbol_exchange
        self.taapi = Taapi(symbol)
        self.time_frame = time_frame
        self.func_entry = func_entry
        self.func_exit = func_exit
        self.logger = logger
        self.bot_object = bot_object
        # self.logger_id = self.logger.objects.create(bot=self.current_bot)
        self.notify = self.user.telegram_notifications
        self.live = self.user.exchange.live

        self.exchange = BinanceHelper(
            api_key=self.user.exchange.api_key,
            api_secret=self.user.exchange.api_secret,
            symbol=self.symbol_exchange,
            user=self.user,
            leverage=self.user.exchange.leverage,
        )

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
            'taapi': self.taapi,
            'symbol': self.symbol,
            'symbol_exchange': self.symbol_exchange,
            'type': -1,
            'time_frame': self.time_frame,
            'ratio': self.func_entry.ratio,
            'takeprofit_value_long': self.func_exit.takeprofit_value_long,
            'takeprofit_value_short': self.func_exit.takeprofit_value_short,
            'stoploss_value_long': self.func_exit.stoploss_value_long,
            'stoploss_value_short': self.func_exit.stoploss_value_short,
            'entry_function': False,
            'exit_function': False,
            'user': self.user.username
        }

    def start(self) -> None:

        if self.notify:
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            start = "Started: " + str(self.current_bot.name) + \
                    "\n" + "User: " + self.user.username + \
                    "\n" + "Balance: " + str(self.exchange.get_current_balance_futures_()) + \
                    "\n" + "Quantity of investement: " + str(self.exchange.get_quantity_from_number_of_bot()) + \
                    "\n" + "Leverage: " + str(self.exchange.leverage) + \
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

                type = ''
                if self.item.get('type') == 0:
                    # LONG
                    type = 'LONG'
                    self.item['takeprofit_ratio'] = round(
                        self.item.get('entry_candle') * self.item.get('takeprofit_value_long'), 3)
                    self.item['stoploss_ratio'] = round(
                        self.item.get('entry_candle') * self.item.get('stoploss_value_long'), 3)

                elif self.item.get('type') == 1:
                    # SHORT
                    type = 'SHORT'
                    self.item['takeprofit_ratio'] = round(
                        self.item.get('entry_candle') * self.item.get('takeprofit_value_short'), 3)
                    self.item['stoploss_ratio'] = round(
                        self.item.get('entry_candle') * self.item.get('stoploss_value_short'), 3)
                self.item['type_text'] = type

                if self.live:
                    if self.item.get('type') == 0:
                        # LONG
                        self.exchange.buy_market()
                    if self.item.get('type') == 1:
                        # SHORT
                        self.exchange.sell_market()

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    entry_text = "Entry: " + str(self.current_bot.name) + \
                                 "\n" + "User: " + self.user.username + \
                                 "\nType Entry: " + self.item.get('type_text') + \
                                 "\nEntry Candle value: " + str(self.item.get('entry_candle')) + \
                                 "\nEntry Candle date: " + str(now) + \
                                 "\nStoploss ratio: " + str(self.item.get('stoploss_ratio')) + \
                                 "\nTakeprofit ratio: " + str(self.item.get('takeprofit_ratio')) + \
                                 "\n" + "Symbol: " + str(self.symbol) + \
                                 "\nTime frame: " + str(self.time_frame)
                    self.telegram.send(entry_text)

                return True

            print(self.item)
            sleep(self.item.get('sleep_func_entry'))

    def exit(self) -> bool:

        func_exit = eval(self.func_exit.name)
        if self.item.get('entry') is True:
            func_exit(item=self.item, bot=True)

            """
            Stoploss
            """
            if self.item.get('stoploss'):

                if self.live:
                    if self.item.get('type') == 0:
                        # LONG
                        self.exchange.sell_market()

                    if self.item.get('type') == 1:
                        # SHORT
                        self.exchange.buy_market()

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    stop_loss = "Stoploss: " + str(self.current_bot.name) + \
                                "\n" + "Current Balance: " + str(self.exchange.get_current_balance_futures_()) + \
                                "\n" + "User: " + self.user.username + \
                                "\nType Entry: " + self.item.get('type_text') + \
                                "\nStoploss candle value: " + str(self.item.get('stoploss_candle')) + \
                                "\nStoploss candle date: " + str(now) + \
                                "\n" + "Symbol: " + str(self.symbol) + \
                                "\nTime frame: " + str(self.time_frame)
                    self.telegram.send(stop_loss)

                return True

            """
            Takeprofit
            """
            if self.item.get('takeprofit'):

                if self.live:
                    if self.item.get('type') == 0:
                        # LONG
                        self.exchange.sell_market()

                    if self.item.get('type') == 1:
                        # SHORT
                        self.exchange.buy_market()

                if self.notify:
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    stop_loss = "Takeprofit: " + str(self.current_bot.name) + \
                                "\n" + "Current Balance: " + str(self.exchange.get_current_balance_futures_()) + \
                                "\n" + "User: " + self.user.username + \
                                "\nType Entry: " + self.item.get('type_text') + \
                                "\nTakeprofit candle value: " + str(self.item.get('takeprofit_candle')) + \
                                "\nTakeprofit candle date: " + str(now) + \
                                "\n" + "Symbol: " + str(self.symbol) + \
                                "\nTime frame: " + str(self.time_frame)
                    self.telegram.send(stop_loss)

                return True

    def run(self) -> bool:

        self.start()

        entry = False
        exception = False

        while run:

            try:

                if entry is False:
                    if self.entry():
                        # Successfully open position
                        entry = True

                if entry is True:
                    self.item['exit_function'] = True
                    if self.exit():
                        sleep(30)
                        # Successfully close position takeprofit/stoploss
                        break

            except Exception as e:
                exception = "ERROR" + str(e)
                self.telegram.send(exception)
                # if exception stop the bot and open position
                exception = True
                break

        if exception:
            return False
        return True
