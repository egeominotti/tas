import datetime
import sys
import decouple
import json
import redis
from binance import Client
from bot.services.telegram import Telegram
from exchange.model.binance import BinanceHelper
from bot.services.indicator import ClusterRealTimeIndicator
from strategy.models import SymbolExchange

# Logic of bot
from bot.strategy.logic.logic_function import \
    logicexit_bot_rsi_20_bollinger, \
    logicentry_bot_rsi_20_bollinger


class ClusteringBot:

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
        self.symbol = None
        self.time_frame = instance.strategy.time_frame.time_frame
        self.func_entry = instance.strategy.logic_entry
        self.func_exit = instance.strategy.logic_exit
        self.logger_instance = None
        self.indicators = None
        self.live = False
        self.quantity = 0
        self.redis_client = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(self.time_frame)
        self.binance_client = Client(api_key=self.userexchange.api_key, api_secret=self.userexchange.api_secret)
        self.exchange = BinanceHelper(
            client=self.binance_client,
            bot=self.current_bot,
            user=self.user,
        )

        try:
            self.telegram = Telegram()
            self.notify = self.user.telegram_notifications

            self.market = ''
            if self.current_bot.market_spot:
                self.market = 'SPOT'
            if self.current_bot.market_futures:
                self.market = 'FUTURES'

            self.coins = SymbolExchange.objects.filter(market=self.market).order_by('created_at')

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
            'start_balance': 0,
            'end_balance': 0,
            'stoploss': False,
            'entry': False,
            'sleep_func_entry': self.func_entry.sleep,
            'type': -1,
            'time_frame': self.time_frame,
            'ratio': self.func_entry.ratio,
            'takeprofit_value_long': self.func_exit.takeprofit_long,
            'takeprofit_value_short': self.func_exit.takeprofit_short,
            'stoploss_value_long': self.func_exit.stoploss_long,
            'stoploss_value_short': self.func_exit.stoploss_short,
            'entry_function': False,
            'exit_function': False,
            'market': self.market,
            'user': self.user.username
        }

        self.current_bot.running = True
        self.current_bot.save()

    def error(self, e):

        exception = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        print(exception)

        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        start = "Warning Stopped Bot: " + str(self.current_bot.name) + \
                "\n" + "Fatal error: " + str(exception) + \
                "\n" + "User: " + self.user.username + \
                "\nTime frame: " + str(self.time_frame) + \
                "\nStopped at: " + str(now)
        self.telegram.send(start)

        self.current_bot.abort = True
        self.current_bot.running = False
        self.current_bot.save()
        self.telegram.send(str(e))

        sys.exit()

    def entry(self, symbol):

        try:

            self.indicators = ClusterRealTimeIndicator(
                self.current_bot,
                symbol,
                self.time_frame,
                self.redis_client
            )

            self.item['indicators'] = self.indicators

            func_entry = eval(self.func_entry.name)
            if self.item.get('entry') is False:

                # Real time indicator disabled check only prev closed candle
                self.indicators.compute(False)
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

                    self.item['start_balance'] = self.exchange.get_current_balance_futures_()

                    now = datetime.datetime.now()
                    self.logger_instance = self.logger.objects \
                        .create(
                        user=self.user,
                        entry_candle=self.item.get('entry_candle'),
                        entry_candle_date=now,
                        stop_loss_ratio=self.item.get('stoploss_ratio'),
                        take_profit_ratio=self.item.get('takeprofit_ratio'),
                        start_balance=self.item['start_balance'],
                        coin_quantity=self.exchange.get_cluster_quantity(self.symbol),
                        leverage=self.exchange.leverage,
                        short=False,
                        long=False
                    )

                    if self.live:

                        # Calculate quantity
                        self.quantity = self.exchange.get_cluster_quantity(self.symbol)

                        if self.item.get('type') == 0:

                            # LONG
                            if self.current_bot.market_futures:
                                self.exchange.buy_market_futures(self.quantity, self.symbol)

                            if self.current_bot.market_spot:
                                self.exchange.buy_market_spot(self.quantity, self.symbol)

                        if self.item.get('type') == 1:

                            # SHORT
                            if self.current_bot.market_futures:
                                self.exchange.sell_market_futures(self.quantity, self.symbol)

                            if self.current_bot.market_spot:
                                self.exchange.sell_market_spot(self.quantity, self.symbol)

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
                                     "\n" + "Trading Market: " + self.market + \
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

            key = self.symbol + "_" + self.time_frame + "_" + self.market + "_CANDLE"
            value = json.loads(self.redis_client.get(key))
            self.item['candle_close'] = value.get('close')

            func_exit = eval(self.func_exit.name)
            if self.item.get('entry') is True:

                # Real time indicator enabled
                # self.indicators.compute(True)
                func_exit(item=self.item)

                """
                Stoploss Exit
                """

                if self.item.get('stoploss') is True:

                    # self.quantity = self.exchange.get_cluster_quantity(self.symbol)

                    if self.live:

                        if self.item.get('type') == 0:
                            # LONG
                            if self.current_bot.market_futures:
                                self.exchange.sell_market_futures(self.quantity, self.symbol)

                            if self.current_bot.market_spot:
                                self.exchange.sell_market_spot(self.quantity, self.symbol)

                        if self.item.get('type') == 1:
                            # SHORT
                            if self.current_bot.market_futures:
                                self.exchange.buy_market_futures(self.quantity, self.symbol)

                            if self.current_bot.market_spot:
                                self.exchange.buy_market_spot(self.quantity, self.symbol)

                    self.item['end_balance'] = self.exchange.get_current_balance_futures_()
                    profit = round(self.item['end_balance'] - self.item['start_balance'], 2)

                    now = datetime.datetime.now()
                    self.logger.objects.filter(id=self.logger_instance.id) \
                        .update(
                        profit=profit,
                        end_balance=self.item['end_balance'],
                        candle_stop_loss=self.item.get('stoploss_candle'),
                        candle_stop_loss_date=now,
                        stop_loss=True,
                    )

                    if self.notify:
                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        stop_loss = "Stoploss: " + str(self.current_bot.name) + \
                                    "\n" + "User: " + self.user.username + \
                                    "\n" + "Profit: " + str(profit) + \
                                    "\n" + "Live Mode: " + str(self.live) + \
                                    "\n" + "Trading Market: " + self.market + \
                                    "\n" + "Current Balance: " + str(self.exchange.get_current_balance_futures_()) + \
                                    "\nType Entry: " + self.item.get('type_text') + \
                                    "\nStoploss candle value: " + str(self.item.get('stoploss_candle')) + \
                                    "\nStoploss candle date: " + str(now) + \
                                    "\n" + "Symbol: " + str(self.symbol) + \
                                    "\nTime frame: " + str(self.time_frame)
                        self.telegram.send(stop_loss)

                    profit = 0
                    for log in self.logger.objects.filter(user=self.user):
                        profit += log.profit

                    self.current_bot.profit = profit
                    self.current_bot.save()

                    return True

                """
                Takeprofit Exit
                """

                if self.item.get('takeprofit') is True:

                    # self.quantity = self.exchange.get_cluster_quantity(self.symbol)

                    if self.live:

                        if self.item.get('type') == 0:
                            # LONG
                            if self.current_bot.market_futures:
                                self.exchange.sell_market_futures(self.quantity, self.symbol)

                            if self.current_bot.market_spot:
                                self.exchange.sell_market_spot(self.quantity, self.symbol)

                        if self.item.get('type') == 1:
                            # SHORT
                            if self.current_bot.market_futures:
                                self.exchange.buy_market_futures(self.quantity, self.symbol)

                            if self.current_bot.market_spot:
                                self.exchange.buy_market_spot(self.quantity, self.symbol)

                    self.item['end_balance'] = self.exchange.get_current_balance_futures_()
                    profit = round(self.item['end_balance'] - self.item['start_balance'], 2)

                    now = datetime.datetime.now()
                    self.logger.objects.filter(id=self.logger_instance.id) \
                        .update(
                        profit=profit,
                        end_balance=self.item['end_balance'],
                        candle_take_profit=self.item.get('takeprofit_candle'),
                        candle_take_profit_date=now,
                        take_profit=True,
                    )

                    if self.notify:
                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        stop_loss = "Takeprofit: " + str(self.current_bot.name) + \
                                    "\n" + "User: " + self.user.username + \
                                    "\n" + "Profit: " + str(profit) + \
                                    "\n" + "Live Mode: " + str(self.live) + \
                                    "\n" + "Trading Market: " + self.market + \
                                    "\n" + "Current Balance: " + str(self.exchange.get_current_balance_futures_()) + \
                                    "\nType Entry: " + self.item.get('type_text') + \
                                    "\nTakeprofit candle value: " + str(self.item.get('takeprofit_candle')) + \
                                    "\nTakeprofit candle date: " + str(now) + \
                                    "\n" + "Symbol: " + str(self.symbol) + \
                                    "\nTime frame: " + str(self.time_frame)
                        self.telegram.send(stop_loss)

                    profit = 0
                    for log in self.logger.objects.filter(user=self.user):
                        profit += log.profit

                    self.current_bot.profit = profit
                    self.current_bot.save()

                    return True

            return False

        except Exception as e:
            self.error(e)
            self.abort()

            return False

    def abort(self) -> None:

        if not self.bot_object.objects.get(id=self.current_bot.id).running:

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

            sys.exit()

    def run(self) -> None:

        entry = False
        sentinel = False
        found_entry = False

        while True:

            try:

                if entry is False:

                    self.abort()

                    # wait message from websocket when candle is closed
                    message = self.pubsub.get_message()
                    if message is not None and message['type'] == 'message':
                        message = json.loads(message['data'])
                        if message.get('status') is True:

                            for coin in self.coins:
                                self.symbol = coin.symbol
                                self.item['symbol_exchange'] = self.symbol

                                if self.entry(self.symbol):
                                    found_entry = True
                                    break

                            if found_entry:
                                entry = True
                                continue

                if entry is True:

                    self.abort()

                    if self.exit():
                        sentinel = True
                        break

            except Exception as e:
                self.error(e)
                self.abort()

        # end-while-true
        if sentinel:
            self.abort()
            self.current_bot.running = False
            self.current_bot.save()

            sys.exit()
