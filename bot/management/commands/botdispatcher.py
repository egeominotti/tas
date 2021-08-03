from time import sleep

from django.core.management import BaseCommand
from django_q.tasks import async_task
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
                    # print(strategy.symbol_exchange.all())
                    # print(strategy.symbol_taapi.all())
                    # print(strategy.user.all())

                    for user in strategy.user.all():
                        if not Bot.objects.filter(user=user, strategy=strategy).exists():
                            for symbol in strategy.symbol_exchange.all():
                                print(user)
                                print(symbol)
                                print(strategy)
                                # spawn bot
                                #bot = Bot.objects.create(user=user, strategy=strategy)

                    sleep(3)

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
