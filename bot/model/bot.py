import threading

from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
from exchange.model.binance import BinanceHelper

"""
Logic function
"""

from backtest.strategy.logic.logic_function import *


class TradingBot:

    def __init__(
            self,
            current_bot,
            user,
            userexchange,
            symbol,
            symbol_exchange,
            time_frame,
            func_entry,
            func_exit,
            logger,
            bot_object,
    ):

        self.current_bot = current_bot
        self.user = user
        self.userexchange = userexchange
        self.telegram = Telegram()
        self.symbol = symbol
        self.symbol_exchange = symbol_exchange
        self.taapi = Taapi(symbol)
        self.time_frame = time_frame
        self.func_entry = func_entry
        self.func_exit = func_exit
        self.logger = logger
        self.logger_instance = None
        self.bot_object = bot_object
        self.notify = self.user.telegram_notifications

        if self.userexchange is not None:

            self.exchange = BinanceHelper(
                api_key=self.userexchange.api_key,
                api_secret=self.userexchange.api_secret,
                symbol=self.symbol_exchange,
                user=self.user,
                leverage=self.userexchange.leverage,
            )

            if self.userexchange.live:
                self.live = True
            else:
                self.live = False
        else:
            self.live = False

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
            'takeprofit_value_long': self.func_exit.takeprofit_long,
            'takeprofit_value_short': self.func_exit.takeprofit_short,
            'stoploss_value_long': self.func_exit.stoploss_long,
            'stoploss_value_short': self.func_exit.stoploss_short,
            'entry_function': False,
            'exit_function': False,
            'user': self.user.username
        }

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        self.thread = thread

        self.item['thread'] = self.thread
        print("Thread Bot: " + str(self.thread))

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

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                if not self.logger.objects.filter(bot=self.current_bot).exists():
                    self.logger_instance = self.logger.objects.create(
                        bot=self.current_bot,
                        entry_candle=self.item.get('entry_candle'),
                        entry_candle_date=now,
                        stop_loss_ratio=self.item.get('stoploss_ratio'),
                        take_profit_ratio=self.item.get('takeprofit_ratio'),
                        start_balance=self.exchange.get_current_balance_futures_(),
                        coin_quantity=self.exchange.get_quantity_from_number_of_bot(),
                        leverage=self.exchange.leverage
                    )

                if self.notify:
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
            # sleep(self.item.get('sleep_func_entry'))

    def exit(self) -> bool:

        func_exit = eval(self.func_exit.name)

        if self.item.get('entry') is True:

            val = func_exit(item=self.item, bot=True)
            if isinstance(val, Exception):
                exception = "ERROR" + str(val)
                self.telegram.send(exception)
                return False
            """
            Stoploss
            """
            if self.item.get('stoploss') is True:

                if self.live:
                    if self.item.get('type') == 0:
                        # LONG
                        self.exchange.sell_market()

                    if self.item.get('type') == 1:
                        # SHORT
                        self.exchange.buy_market()

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.logger.objects.filter(id=self.logger_instance.id).update(
                    end_balance=self.exchange.get_current_balance_futures_(),
                    candle_stop_loss=self.item.get('stoploss_candle'),
                    candle_stop_loss_date=now,
                    stop_loss=True
                )

                if self.notify:
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
            if self.item.get('takeprofit') is True:

                if self.live:
                    if self.item.get('type') == 0:
                        # LONG
                        self.exchange.sell_market()

                    if self.item.get('type') == 1:
                        # SHORT
                        self.exchange.buy_market()

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.logger.objects.filter(id=self.logger_instance.id).update(
                    end_balance=self.exchange.get_current_balance_futures_(),
                    candle_stop_loss=self.item.get('takeprofit_candle'),
                    candle_stop_loss_date=now,
                    take_profit=True
                )

                if self.notify:
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

        while True:

            try:

                if entry is False:
                    if datetime.datetime.now().second == 59:
                        if self.entry():
                            # Successfully open position
                            entry = True

                if entry is True:
                    self.item['exit_function'] = True
                    if self.exit() is False:
                        exception = True
                        self.bot_object.objects.filter(id=self.current_bot.id).delete()
                        break

                    if self.exit() is True:
                        sleep(30)
                        self.bot_object.objects.filter(id=self.current_bot.id).delete()
                        # Successfully close position takeprofit/stoploss
                        break

            except Exception as e:
                exception = "ERROR" + str(e)
                self.telegram.send(exception)
                self.bot_object.objects.filter(id=self.current_bot.id).delete()
                # if exception stop the bot and open position
                exception = True
                break

        if exception:
            return False
        return True
