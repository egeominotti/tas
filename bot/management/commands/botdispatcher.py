import signal
from time import sleep
from django.core.management import BaseCommand
from django_q.tasks import async_task
from bot.models import Bot, BotLogger
from bot.models import StrategyBot
import logging

logger = logging.getLogger('main')


def handler_stop_signals(signum, frame):
    Bot.objects.all().delete()
    exit(1)


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)


class Command(BaseCommand):
    help = 'DispatcherBot'

    def handle(self, *args, **kwargs):

        while True:

            try:
                qs = StrategyBot.objects.filter(live_mode=True)
                for strategy in qs:
                    for user in strategy.user.all():
                        for coins in strategy.coins.all():
                            if not Bot.objects.filter(user=user, coins=coins).exists():
                                bot = Bot.objects.create(user=user, strategy=strategy, coins=coins)
                                async_task("bot.services.runner.runnerbot",
                                           bot,
                                           user,
                                           coins.coins_taapi.symbol,
                                           coins.coins_exchange.symbol,
                                           Bot,
                                           BotLogger,
                                           hook="bot.services.runner.get_runnerbot_hook")

                sleep(500)
            except Exception as e:
                print(e)
