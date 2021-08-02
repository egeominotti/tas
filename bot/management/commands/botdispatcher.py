from time import sleep

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django_q.tasks import async_task
from analytics.models import TrendChecker
from bot.models import Bot, BotLogger
from strategy.models import Strategy
import logging
from django_q.brokers import get_broker

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'DispatcherBot'

    def handle(self, *args, **kwargs):
        broker = get_broker()
        while True:

            try:

                qs = Strategy.objects.all()
                usr = User.objects.all()
                for user in usr:
                    for strategy in qs:
                        tch = TrendChecker.objects.filter(symbol=strategy.symbol_exchange,
                                                          time_frame=strategy.time_frame).first()

                        if tch.trade_long is True and strategy.long is True:
                            if not Bot.objects.filter(strategy=strategy, user=user).exists():
                                bot = Bot.objects.create(strategy=strategy, user=user)
                                print("avvio bot con strategia long")

                                async_task("bot.services.runner.runnerbot",
                                           bot,
                                           Bot,
                                           BotLogger,
                                           hook="bot.services.runner.get_runnerbot_hook", broker=broker)

                        if tch.trade_short is True and strategy.short is True:
                            if not Bot.objects.filter(strategy=strategy, user=user).exists():
                                bot = Bot.objects.create(strategy=strategy, user=user)
                                print("avvio bot con strategia short")

                                async_task("bot.services.runner.runnerbot",
                                           bot,
                                           Bot,
                                           BotLogger,
                                           hook="bot.services.runner.get_runnerbot_hook", broker=broker)

                sleep(15)

            except Exception as e:
                print(e)
                Bot.objects.all().delete()
