import signal
from time import sleep
from django.core.management import BaseCommand
from django_q.tasks import async_task
from bot.models import Bot, BotLogger
from bot.models import StrategyBot
import logging
from bot.models import UserExchange
from django_q.brokers import get_broker

logger = logging.getLogger('main')


def handler_stop_signals(signum, frame):
    exit(1)


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)


class Command(BaseCommand):
    help = 'RunnerSingleBot'

    def handle(self, *args, **kwargs):
        broker = get_broker()

        try:

            qs = StrategyBot.objects.all() \
                .select_related('logic_entry') \
                .select_related('logic_exit') \
                .select_related('time_frame') \
                .prefetch_related('coins') \
                .prefetch_related('user')

            for strategy in qs:
                for user in strategy.user.all():
                    userexchange = UserExchange.objects.get(user=user)
                    for coins in strategy.coins.all():
                        if not Bot.objects.filter(user=user, coins=coins).exists():
                            bot = Bot.objects.create(user=user, strategy=strategy, coins=coins)
                            user.counter_bot = strategy.coins.count()
                            user.save()
                            async_task("bot.services.runner.runnerbot",
                                       bot,
                                       user,
                                       userexchange,
                                       coins.coins_taapi.symbol,
                                       coins.coins_exchange.symbol,
                                       Bot,
                                       BotLogger,
                                       broker=broker,
                                       cached=True,
                                       hook="bot.services.runner.get_runnerbot_hook")

                            # wait for taapi
                            sleep(15)
            # wait 10 minutes
            sleep(300)
        except Exception as e:
            print(e)
