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
                    for user in strategy.user.all():
                        print(user)
                        for coins in strategy.coins.all():
                            print(coins.coins_exchange.symbol)
                            if not Bot.objects.filter(user=user, strategy=strategy).exists():
                                bot = Bot.objects.create(user=user, strategy=strategy)
                                async_task("bot.services.runner.runnerbot",
                                           coins.coins_taapi.symbol,
                                           coins.coins_exchange.symbol,
                                           bot,
                                           Bot,
                                           BotLogger,
                                           hook="bot.services.runner.get_runnerbot_hook")

                sleep(300)
            except Exception as e:
                print(e)
