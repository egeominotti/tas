from time import sleep

from django.core.management import BaseCommand
import logging
from bot.model.bot import TradingBot
from bot.models import Bot, UserExchange, BotLogger

logger = logging.getLogger('main')


def spawnbot(instance) -> None:
    TradingBot(
        current_bot=instance,
        user=instance.user,
        userexchange=UserExchange.objects.get(user=instance.user),
        symbol=instance.coins.coins_taapi.symbol,
        symbol_exchange=instance.coins.coins_exchange.symbol,
        time_frame=instance.strategy.time_frame.time_frame,
        func_entry=instance.strategy.logic_entry,
        func_exit=instance.strategy.logic_exit,
        logger=BotLogger,
        bot_object=Bot,
    )
    instance.running = True
    instance.save()


def init() -> None:
    while True:
        sleep(60)
        for instance in Bot.objects.filter(running=False):
            spawnbot(instance)


class Command(BaseCommand):
    help = 'AsyncBotRunner'

    def handle(self, *args, **kwargs):
        init()
