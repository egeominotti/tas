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
            print(bot.strategy.symbol_exchange)
            print(bot.strategy.time_frame)
            tch = TrendChecker.objects.filter(symbol=bot.strategy.symbol_exchange, time_frame=bot.strategy.time_frame)
            print(tch)
            if bot.status != 'START':
                async_task("bot.services.runner.runnerbot", bot, Bot, BotLogger)
                bot.status = 'START'
                bot.save()
            # Se l'andmento è long allora avvio bot long

            # Se l'andamento è short allora avvio bot shot
