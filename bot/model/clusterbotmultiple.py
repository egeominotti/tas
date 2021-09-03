import datetime
import sys
from threading import Thread

import decouple
import json
import redis
from binance import Client
from bot.services.telegram import Telegram
from exchange.model.binance import BinanceHelper
from strategy.models import SymbolExchange
from bot.model.bot import TradeBot

# Logic of bot
from bot.strategy.logic.logic_function import \
    logicexit_bot_rsi_20_bollinger, \
    logicentry_bot_rsi_20_bollinger


class ClusteringBotMultiple:

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
        self.redis_client = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)

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

        self.current_bot.running = True
        self.current_bot.save()

    def error(self, e):

        exception = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        print(exception)

        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        start = "Warning Stopped Bot: " + str(self.current_bot.name) + \
                "\n" + "Fatal error: " + str(exception) + \
                "\n" + "User: " + self.user.username + \
                "\nStopped at: " + str(now)
        self.telegram.send(start)

        self.current_bot.abort = True
        self.current_bot.running = False
        self.current_bot.save()
        self.telegram.send(str(e))

        sys.exit()


    def run(self) -> None:

        try:
            for coin in self.coins:
                print(coin)

                tb = TradeBot(
                    self.current_bot,
                    self.userexchange,
                    self.logger,
                    coin.symbol,
                    self.redis_client
                )

                thread = Thread(target=tb.run, args=())
                thread.daemon = True
                thread.start()
                thread.join()

        except Exception as e:
            self.error(e)
