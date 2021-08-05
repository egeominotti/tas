import threading
from time import sleep
from django.core.management import BaseCommand
import logging
from bot.model.bot import TradingBot
from bot.models import Bot, UserExchange, StrategyBot, BotLogger

logger = logging.getLogger('main')


def spawnbot(bot, user, userexchange, coins) -> None:

    TradingBot(
        current_bot=bot,
        user=user,
        userexchange=userexchange,
        symbol=coins.coins_taapi.symbol,
        symbol_exchange=coins.coins_exchange.symbol,
        time_frame=bot.strategy.time_frame.time_frame,
        func_entry=bot.strategy.logic_entry,
        func_exit=bot.strategy.logic_exit,
        logger=BotLogger,
        bot_object=Bot
    )


def init() -> None:
    while True:

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
                            spawnbot(bot, user, userexchange, coins)
                            sleep(15)

            sleep(300)

        except Exception as e:
            print(e)
            break


class Command(BaseCommand):
    help = 'AsyncBotRunner'

    def handle(self, *args, **kwargs):
        t = threading.Thread(target=init)
        t.start()
