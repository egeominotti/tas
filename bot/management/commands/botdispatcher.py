from time import sleep

from django.core.management import BaseCommand
from django_q.tasks import async_task
from analytics.models import TrendChecker
from bot.models import Bot, BotLogger
from bot.models import StrategyBot
import logging
from exchange.model.binance import BinanceHelper

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'DispatcherBot'

    def handle(self, *args, **kwargs):

        while True:

            try:
                qs = StrategyBot.objects.filter(live_mode=True)
                for strategy in qs:

                    bh = BinanceHelper(
                        api_key=strategy.user.exchange.api_key,
                        api_secret=strategy.user.exchange.api_secret,
                        symbol=strategy.symbol_exchange.symbol
                    )
                    print(strategy.symbol_exchange.symbol)
                    print(bh.get_current_balance_futures_())
                    print(bh.get_symbol_precision())
                    print(bh.current_price_coin())
                    print(bh.get_quantity())
                    sleep(3)

                    # if not Bot.objects.filter(strategy=strategy).exists():
                    #     bot = Bot.objects.create(strategy=strategy)


                    # BotLogger.objects.create(
                    #     bot=bot,
                    #
                    # )
                    # async_task("bot.services.runner.runnerbot",
                    #            bot,
                    #            Bot,
                    #            BotLogger,
                    #            hook="bot.services.runner.get_runnerbot_hook")

                # sleep(300)
            except Exception as e:
                print(e)
