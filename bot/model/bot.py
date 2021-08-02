from time import sleep
import datetime
from bot.services.telegram import Telegram
from analytics.services.exchangeApi import Taapi
import schedule
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
        self.item = {
            'symbol': self.symbol,
            'type': self.func_exit.short or self.func_exit.long,
            'time_frame': self.time_frame,
            'ratio': self.func_entry.ratio,
            'stop_loss': self.func_exit.stop_loss,
            'take_profit': self.func_exit.take_profit,
            'sleep_func_entry': self.func_entry.sleep,
            'sleep_func_exit': self.func_exit.sleep,
            'taapi': self.taapi,
            'entry': False,
            'is_take_profit': False,
            'is_stop_loss': False
        }

    def start(self):
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        start = "Started: " + str(self.current_bot.name) + \
                "\n" + "Symbol: " + str(self.symbol) + \
                "\nTime frame: " + str(self.time_frame) + \
                "\nStarted at: " + str(now) + \
                "\nLet's go to the moon 🚀️"
        self.telegram.send(start)

    def entry(self):
        print("funzione entry")
        func_entry = eval(self.func_entry.name)
        if self.item.get('entry') is False:
            func_entry(item=self.item, bot=True)
            print(self.item)
            if self.item.get('entry') is True:
                self.exit()

    def exit(self):
        print("funzione exit")
        func_exit = eval(self.func_exit.name)
        if self.item.get('entry') is True:
            func_exit(item=self.item, bot=True)
            print(self.item)
            if self.item.get('is_stop_loss') is True or self.item.get('is_take_profit') is True:
                exit(1)

    def run(self):

        schedule.every(self.item.get('sleep_func_entry')).minute.do(self.entry)

        while True:
            schedule.run_pending()
            sleep(1)
        # self.start()

        # while True:
        #     try:
        #
        #         if item.get('entry') is False:
        #             func_entry(item=item, bot=True)
        #             print(item)
        #             sleep(item.get('sleep_func_entry'))
        #             continue
        #
        #         if item.get('entry') is True:
        #
        #             func_exit(item=item, bot=True)
        #             print(item)
        #             if item.get('is_stop_loss') is True or item.get('is_take_profit') is True:
        #                 break
        #
        #             sleep(item.get('sleep_func_exit'))
        #             continue
        #
        #     except Exception as e:
        #         print(str(e))
        #         break

        # while True:

        #
        # try:
        #
        #     """
        #     Finche non viene trovata una entry utile continua ad eseguire
        #     """
        #     if position is False:
        #
        #         func_entry_value = self.func_entry(item=item, bot=True)
        #         if isinstance(func_entry_value, Exception):
        #             error = "ERROR" + str(func_entry_value)
        #             self.telegram.send(error)
        #
        #         if isinstance(func_entry_value, float):
        #             now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        #             entry_text = "Bot: " + str(self.current_bot.name) + \
        #                          "\n" + "Symbol: " + str(self.symbol) + \
        #                          "\nTime frame: " + str(self.time_frame) + \
        #                          "\nEntry Candle value: " + str(func_entry_value) + \
        #                          "\nEntry Candel date: " + str(now)
        #             self.telegram.send(entry_text)
        #
        #             now = datetime.datetime.now()
        #             self.logger.objects.filter(id=self.logger_id.id).update(
        #                 entry_candle=func_entry_value,
        #                 entry_candle_date=now,
        #             )
        #
        #             # if self.current_bot.live:
        #             #     self.binance.buy()
        #
        #             open_position_value = func_entry_value
        #             position = True
        #
        #     sleep(sleep_time_position)
        #
        #     """
        #     Se viene aperta una posizione allora verifica le condizioni stoploss e takeprofit
        #     """
        #     if position is True:
        #         print("Provo a cercare una take profit o stop loss")
        #         value = self.func_exit(item=item, bot=True)
        #
        #         if isinstance(value, Exception):
        #             error = "ERROR" + str(value)
        #             self.telegram.send(error)
        #             break
        #
        #         if isinstance(value, float):
        #             now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        #             stop_loss = "Bot: " + str(self.current_bot.name) + \
        #                         "\n" + "Symbol: " + str(self.symbol) + \
        #                         "\nTime frame: " + str(self.time_frame) + \
        #                         "\nStop loss candle value: " + str(value) + \
        #                         "\nStop loss candle date: " + str(now)
        #             self.telegram.send(stop_loss)
        #
        #             now = datetime.datetime.now()
        #             self.logger.objects.filter(id=self.logger_id.id).update(
        #                 candle_take_profit=value,
        #                 candle_take_profit_date=now,
        #                 stop_loss=True,
        #             )
        #             #
        #             # if self.current_bot.live:
        #             #     self.binance.sell()
        #
        #             break
        #
        #         # value = self.func_take_profit(item=item, bot=True)
        #         # if isinstance(value, Exception):
        #         #     error = "ERROR" + str(value)
        #         #     self.telegram.send(error)
        #         #     break
        #         #
        #         # if isinstance(value, float):
        #         #
        #         #     now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        #         #     take_profit = "Bot: " + str(self.current_bot.name) + \
        #         #                  "\n" + "Symbol: " + str(self.symbol) + \
        #         #                  "\nTime frame: " + str(self.time_frame) + \
        #         #                  "\nTake Profit candle value: " + str(value) + \
        #         #                  "\nTake profit candle date: " + str(now)
        #         #     self.telegram.send(take_profit)
        #         #
        #         #     now = datetime.datetime.now()
        #         #     self.logger.objects.filter(id=self.logger_id.id).update(
        #         #         candle_stop_loss=value,
        #         #         candle_stop_loss_date=now,
        #         #         take_profit=True,
        #         #     )
        #
        #         # if self.current_bot.live:
        #         #     self.binance.sell()
        #
        #
        #
        #
        # except Exception as e:
        #     start = "Errore imprevisto nel bot: " + str(e)
        #     self.telegram.send(start)
        #     break
