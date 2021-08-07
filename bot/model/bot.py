from time import sleep

from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
from exchange.model.binance import BinanceHelper
from backtest.strategy.logic.logic_function import *


class TradingBot:

    def __init__(self,
                 current_bot,
                 user,
                 userexchange,
                 symbol,
                 symbol_exchange,
                 time_frame,
                 func_entry,
                 func_exit,
                 logger,
                 bot_object):

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
        self.bot_object = bot_object
        self.notify = self.user.telegram_notifications
        self.process = None
        self.logger_instance = None

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

    def error(self, e, func):
        exception = "ERROR" + str(e) + " function:" + str(func)
        print("ERROR" + str(e) + " function:" + str(func))
        self.telegram.send(exception)

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

        try:

            func_entry = eval(self.func_entry.name)
            if self.item.get('entry') is False:
                func_entry(item=self.item, bot=True)

                print(self.item)

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

                    now = datetime.datetime.now()
                    self.logger_instance = self.logger.objects \
                        .create(
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

        except Exception as e:
            self.error(e, self.func_entry.name)
            return False

    def exit(self) -> bool:

        try:
            func_exit = eval(self.func_exit.name)
            if self.item.get('entry') is True:
                func_exit(item=self.item, bot=True)

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

                    now = datetime.datetime.now()
                    self.logger.objects.filter(id=self.logger_instance.id) \
                        .update(
                        end_balance=self.exchange.get_current_balance_futures_(),
                        candle_stop_loss=self.item.get('takeprofit_candle'),
                        candle_stop_loss_date=now,
                        take_profit=True
                    )

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

        except Exception as e:
            self.error(e, self.func_entry.name)
            return False

    def abort(self):
        if self.bot_object.objects.get(id=self.current_bot.id).abort:
            return True
        else:
            return False

    def run(self) -> None:

        self.start()

        entry = False
        while True:

            try:

                if entry is False:
                    if datetime.datetime.now().second == 59:
                        if self.entry():
                            if self.abort():
                                print("Esco dal bot")
                                self.current_bot.running = False
                                self.current_bot.save()
                                break
                            else:
                                print("HO TROVATO UNA ENTRY")
                                print(self.item)
                                entry = True
                                self.current_bot.running = False
                                self.current_bot.save()
                                print("Esco dal bot")
                                continue
                                # Successfully open position

                if entry is True:
                    self.item['exit_function'] = True
                    if self.exit():
                        print("HO TROVATO UNO STOP LOSS O TAKE PROFIT RINIZIO DA CAPO A CERCARE")
                        sleep(5)
                        print("value abort: " + self.current_bot.objects.get(id=self.current_bot.id).abort)
                        if self.abort():
                            break
                        else:
                            print("Esco dal bot")
                            self.current_bot.running = False
                            self.current_bot.save()
                            entry = False
                            continue

            except Exception as e:
                print(e)
                self.error(e, 'run')
                sleep(5)
                continue
