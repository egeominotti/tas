from threading import Thread
from bot.model.clusterbot import ClusterBot
from bot.models import Bot, ClusterBot, UserExchange, BotLogger
from django.core.management import BaseCommand
from time import sleep
import logging
import os

logger = logging.getLogger('main')


def spawnbot(instance) -> None:

    tb = ClusterBot(
        instance=instance,
        userexchange=UserExchange.objects.get(user=instance.user),
        logger=BotLogger,
        bot_object=Bot,
    )
    tb.run()


def init() -> None:

    while True:
        qs = ClusterBot.objects.filter(running=False, abort=False).all()
        print(qs)
        # if qs.count() > 0:
        #     for instance in qs:
        #         thread = Thread(target=spawnbot, name=instance.name, args=(instance,))
        #         thread.daemon = True
        #         instance.running = True
        #         instance.save()
        #         thread.start()
        #         print("Sart thread: " + str(thread))
        sleep(1)


class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):
        init()
