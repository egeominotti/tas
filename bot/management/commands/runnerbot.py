import datetime
from threading import Thread
from time import sleep
from django.core.management import BaseCommand
import logging
from bot.model.bot import TradingBot
from bot.models import Bot, UserExchange, BotLogger

logger = logging.getLogger('main')


def spawnbot(instance) -> None:

    tb = TradingBot(
        instance=instance,
        userexchange=UserExchange.objects.get(user=instance.user),
        logger=BotLogger,
        bot_object=Bot,
    )
    tb.run()


def init() -> None:
    while True:

        if datetime.datetime.now().second == 30:
            qs = Bot.objects.filter(running=False, abort=False)
            if qs.count() > 0:
                for instance in qs:
                    thread = Thread(target=spawnbot, name=instance.name, args=(instance,))
                    thread.daemon = True
                    instance.running = True
                    instance.save()
                    thread.start()
                    print("Sart thread: " + str(thread))

                    # For taapi
                    sleep(15)


class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):
        init()
