from threading import Thread

import multiprocessing

from bot.model.clusterbot import ClusteringBot
from bot.models import ClusterBot, UserExchange, BotLogger
from django.core.management import BaseCommand
from time import sleep
import logging

logger = logging.getLogger('main')


def spawnbot(instance) -> None:

    tb = ClusteringBot(
        instance=instance,
        userexchange=UserExchange.objects.get(user=instance.user),
        logger=BotLogger,
        bot_object=ClusterBot,
    )
    tb.run()


def init() -> None:

    while True:
        qs = ClusterBot.objects.filter(running=False, abort=False)
        if qs.count() > 0:
            for instance in qs:
                process = multiprocessing.Process(target=spawnbot, name=instance.name, args=(instance,))
                process.daemon = True
                instance.running = True
                instance.save()
                process.start()
                print("Sart process: " + str(process))

        sleep(0.1)


class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):
        init()
