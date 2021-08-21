from time import sleep
import sys
from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
from exchange.model.binance import BinanceHelper
from bot.strategy.logic.logic_function import *


class TradingBot:

    def __init__(
            self,
            instance,
            userexchange,
            logger,
            bot_object
    ):
        """

        :param instance: Istanza del bot
        :param userexchange:  Exchange dell'utente
        :param logger:  Oggetto logger queryset
        :param bot_object:  Oggetto bot queryset
        """

        self.current_bot = instance
        self.logger = logger
        self.bot_object = bot_object
        self.user = instance.user
        self.userexchange = userexchange
        self.symbol = instance.coins.coins_taapi.symbol
        self.symbol_exchange = instance.coins.coins_exchange.symbol
        self.time_frame = instance.strategy.time_frame.time_frame
        self.func_entry = instance.strategy.logic_entry
        self.func_exit = instance.strategy.logic_exit
        self.logger_instance = None
        self.live = False
        self.quantity = 0

        try:

            self.telegram = Telegram()
            self.notify = self.user.telegram_notifications
            self.taapi = Taapi(self.symbol)
            self.indicators = RealTimeIndicator(self.symbol, self.time_frame, self.userexchange.api_key, self.userexchange.api_secret)
            self.exchange = BinanceHelper(
                bot=self.current_bot,
                api_key=self.userexchange.api_key,
                api_secret=self.userexchange.api_secret,
                symbol=self.symbol_exchange,
                user=self.user,
            )

            if self.current_bot.live:
                self.live = True

        except Exception as e:
            self.error(e)
            self.abort()

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
            'indicators':  self.indicators,
            'entry_function': False,
            'exit_function': False,
            'user': self.user.username
        }

        try:
            self.current_bot.running = True
            self.current_bot.save()
            self.start()

        except Exception as e:
            self.error(e)
            self.abort()

    def error(self, e):

        exception = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        print(exception)

        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        start = "Warning Stopped Bot: " + str(self.current_bot.name) + \
                "\n" + "Fatal error: " + str(exception) + \
                "\n" + "User: " + self.user.username + \
                "\n" + "Symbol: " + str(self.symbol) + \
                "\nTime frame: " + str(self.time_frame) + \
                "\nStopped at: " + str(now)
        self.telegram.send(start)

        self.current_bot.abort = True
        self.current_bot.running = False
        self.current_bot.save()
        # logger.error(exception)
        self.telegram.send(str(e))
        exit(1)

    def start(self) -> None:

        if self.notify:
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            start = "Started: " + str(self.current_bot.name) + \
                    "\n" + "User: " + self.user.username + \
                    "\n" + "Balance: " + str(self.exchange.get_current_balance_futures_()) + \
                    "\n" + "Live Mode: " + str(self.live) + \
                    "\n" + "Investment amount: " + str(self.exchange.get_current_investment_amount()) + \
                    "\n" + "Quantity of investement: " + str(self.exchange.get_quantity()) + \
                    "\n" + "Leverage: " + str(self.exchange.leverage) + \
                    "\n" + "Symbol: " + str(self.symbol) + \
                    "\nTime frame: " + str(self.time_frame) + \
                    "\nStarted at: " + str(now) + \
                    "\nLet's go to the moon 🚀️"
            self.telegram.send(start)

    def entry(self) -> bool:

        try:

            func_entry = eval(self.func_entry.name)
            if self.item.get('entry') is False:
                func_entry(item=self.item)

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

                    now = datetime.datetime.now()
                    self.logger_instance = self.logger.objects \
                        .create(
                        user=self.user,
                        entry_candle=self.item.get('entry_candle'),
                        entry_candle_date=now,
                        stop_loss_ratio=self.item.get('stoploss_ratio'),
                        take_profit_ratio=self.item.get('takeprofit_ratio'),
                        start_balance=self.exchange.get_current_balance_futures_(),
                        coin_quantity=self.exchange.get_quantity(),
                        leverage=self.exchange.leverage,
                        short=False,
                        long=False
                    )

                    if self.live:

                        # Calculate quantity
                        self.quantity = self.exchange.get_quantity()

                        if self.item.get('type') == 0:
                            # LONG
                            self.exchange.buy_market(self.quantity)

                        if self.item.get('type') == 1:
                            # SHORT
                            self.exchange.sell_market(self.quantity)

                    if self.item.get('type') == 0:
                        self.logger.objects.filter(id=self.logger_instance.id) \
                            .update(
                            long=True
                        )

                    if self.item.get('type') == 1:
                        self.logger.objects.filter(id=self.logger_instance.id) \
                            .update(
                            short=True
                        )

                    if self.notify:
                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        entry_text = "Entry: " + str(self.current_bot.name) + \
                                     "\n" + "User: " + self.user.username + \
                                     "\nType Entry: " + self.item.get('type_text') + \
                                     "\n" + "Live Mode: " + str(self.live) + \
                                     "\nEntry Candle value: " + str(self.item.get('entry_candle')) + \
                                     "\nEntry Candle date: " + str(now) + \
                                     "\nStoploss ratio: " + str(self.item.get('stoploss_ratio')) + \
                                     "\nTakeprofit ratio: " + str(self.item.get('takeprofit_ratio')) + \
                                     "\n" + "Symbol: " + str(self.symbol) + \
                                     "\nTime frame: " + str(self.time_frame)
                        self.telegram.send(entry_text)

                    return True

        except Exception as e:
            self.error(e)
            self.abort()

    def exit(self) -> bool:

        try:

            func_exit = eval(self.func_exit.name)
            if self.item.get('entry') is True:
                func_exit(item=self.item)

                """
                Stoploss
                """
                if self.item.get('stoploss') is True:

                    if self.live:
                        if self.item.get('type') == 0:
                            # LONG
                            self.exchange.sell_market(self.quantity)

                        if self.item.get('type') == 1:
                            # SHORT
                            self.exchange.buy_market(self.quantity)

                    now = datetime.datetime.now()
                    self.logger.objects.filter(id=self.logger_instance.id) \
                        .update(
                        end_balance=self.exchange.get_current_balance_futures_(),
                        candle_stop_loss=self.item.get('stoploss_candle'),
                        candle_stop_loss_date=now,
                        stop_loss=True
                    )

                    if self.notify:
                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        stop_loss = "Stoploss: " + str(self.current_bot.name) + \
                                    "\n" + "Live Mode: " + str(self.live) + \
                                    "\n" + "Current Balance: " + str(self.exchange.get_current_balance_futures_()) + \
                                    "\n" + "Investement: " + str(self.exchange.get_current_investment_amount()) + \
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
                            self.exchange.sell_market(self.quantity)

                        if self.item.get('type') == 1:
                            # SHORT
                            self.exchange.buy_market(self.quantity)

                    now = datetime.datetime.now()
                    self.logger.objects.filter(id=self.logger_instance.id) \
                        .update(
                        end_balance=self.exchange.get_current_balance_futures_(),
                        candle_take_profit=self.item.get('takeprofit_candle'),
                        candle_take_profit_date=now,
                        take_profit=True
                    )

                    if self.notify:
                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        stop_loss = "Takeprofit: " + str(self.current_bot.name) + \
                                    "\n" + "Live Mode: " + str(self.live) + \
                                    "\n" + "Current Balance: " + str(self.exchange.get_current_balance_futures_()) + \
                                    "\n" + "Investement: " + str(self.exchange.get_current_investment_amount()) + \
                                    "\n" + "User: " + self.user.username + \
                                    "\nType Entry: " + self.item.get('type_text') + \
                                    "\nTakeprofit candle value: " + str(self.item.get('takeprofit_candle')) + \
                                    "\nTakeprofit candle date: " + str(now) + \
                                    "\n" + "Symbol: " + str(self.symbol) + \
                                    "\nTime frame: " + str(self.time_frame)
                        self.telegram.send(stop_loss)

                    return True

        except Exception as e:
            self.error(e)
            self.abort()

    def abort(self) -> None:
        if not self.bot_object.objects.get(id=self.current_bot.id).running:

            logger.info("Set bot not running and close position")
            self.current_bot.abort = True
            self.current_bot.running = False
            self.current_bot.save()

            try:
                self.exchange.futures_cancel_order_()
            except Exception as e:
                self.error(e)

            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            start = "Aborted bot: " + str(self.current_bot.name) + \
                    "\n" + "User: " + self.user.username + \
                    "\n" + "Symbol: " + str(self.symbol) + \
                    "\nTime frame: " + str(self.time_frame) + \
                    "\nAborted at: " + str(now)
            self.telegram.send(start)

            sleep(5)
            exit(1)

    def run(self) -> None:

        entry = False
        sentinel = False

        while True:

            try:

                if entry is False:

                    self.abort()
                    if self.entry():
                        self.abort()

                        print("Found Entry: " + str(self.item))
                        logger.info("Found Entry: " + str(self.item))
                        entry = True
                        continue

                if entry is True:

                    self.abort()

                    if self.exit():
                        self.item['exit_function'] = True
                        """
                        FOUND EXIT
                        """
                        print("Found stoploss or takeprofit : " + str(self.item))
                        logger.info("Found stoploss or takeprofit : " + str(self.item))
                        self.abort()

                        entry = False
                        sentinel = True
                        break

            except Exception as e:
                self.error(e)
                self.abort()

        # end-while-true
        self.abort()
        if sentinel:
            print("Exit bot normally set running = False : " + str(self.item))

            self.abort()

            # Set running = False for restart bot
            self.current_bot.running = False
            self.current_bot.save()

            sleep(30)
            exit(1)
