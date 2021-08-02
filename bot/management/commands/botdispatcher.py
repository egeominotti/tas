from django.core.management import BaseCommand
from django_q.tasks import async_task
from analytics.models import TrendChecker
from bot.models import Bot, BotLogger
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'DispatcherBot'

    def handle(self, *args, **kwargs):
        qs = Bot.objects.all()
        for bot in qs:
            tch = TrendChecker.objects.filter(symbol=bot.strategy.symbol_exchange,
                                              time_frame=bot.strategy.time_frame).first()

            if tch.trade_long is True and bot.status != 'START' and bot.long is True:
                print("avvio bot con strategia long")
                bot.status = 'START'
                bot.save()
                async_task("bot.services.runner.runnerbot", bot, Bot, BotLogger)

            if tch.trade_short is True and bot.status != 'START' and bot.short is True:
                print("avvio bot con strategia short")
                bot.status = 'START'
                bot.save()
                async_task("bot.services.runner.runnerbot", bot, Bot, BotLogger)
