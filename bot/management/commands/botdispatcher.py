from time import sleep

from django.core.management import BaseCommand
from django_q.tasks import async_task
from analytics.models import TrendChecker
from bot.models import Bot, BotLogger
from strategy.models import Strategy
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'DispatcherBot'

    def handle(self, *args, **kwargs):

        qs = Strategy.objects.all()
        for strategy in qs:

            tch = TrendChecker.objects.filter(symbol=strategy.symbol_exchange,
                                              time_frame=strategy.time_frame).first()

            if tch.trade_long is True and strategy.long is True:
                bot = Bot.objects.create(strategy=strategy)
                print("avvio bot con strategia long")
                async_task("bot.services.runner.runnerbot", bot, Bot, BotLogger)

            if tch.trade_short is True and strategy.short is True:
                bot = Bot.objects.create(strategy=strategy)
                print("avvio bot con strategia short")
                async_task("bot.services.runner.runnerbot", bot, Bot, BotLogger)
