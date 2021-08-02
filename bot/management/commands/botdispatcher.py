from django.core.management import BaseCommand
from django_q.tasks import async_task

from bot.models import Bot, BotLogger
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'DispatcherBot'

    def handle(self, *args, **kwargs):
        qs = Bot.objects.all().exclude(status='START')
        for bot in qs:
            async_task("bot.services.runner.runnerbot", bot, Bot, BotLogger)
            bot.status = 'START'
            bot.save()
            # Se l'andmento è long allora avvio bot long

            # Se l'andamento è short allora avvio bot shot

