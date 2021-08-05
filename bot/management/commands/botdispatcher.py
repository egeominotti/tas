import threading
from time import sleep
from multiprocessing import Process
from django.core.management import BaseCommand
import logging
from bot.model.bot import TradingBot
from bot.models import Bot, UserExchange, StrategyBot, BotLogger

logger = logging.getLogger('main')

def asyncspawnbot(bot, user, userexchange, coins) -> None:

    print(coins.coins_exchange.symbol)
    print(coins.coins_taapi.symbol)
    print("avvio bot")
    bot = TradingBot(
        current_bot=bot,
        user=user,
        userexchange=userexchange,
        symbol=coins.coins_exchange.symbol,
        symbol_exchange=coins.coins_taapi.symbol,
        time_frame=bot.strategy.time_frame.time_frame,
        func_entry=bot.strategy.logic_entry,
        func_exit=bot.strategy.logic_exit,
        logger=BotLogger,
        bot_object=Bot
    )

    if bot.run():
        Bot.objects.filter(id=bot.id).delete()


def init() -> None:

    while True:

        try:
            process = []
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
                            print("avvio")
                            user.counter_bot = strategy.coins.count()
                            user.save()

                            # asyncspawnbot(bot, user, userexchange, coins)
                            t = threading.Thread(target=asyncspawnbot, args=(bot, user, userexchange, coins,))
                            t.start()
                            process.append(t)

                            sleep(15)
            print(process)
            sleep(300)

        except Exception as e:
            print(e)
            break


class Command(BaseCommand):
    help = 'AsyncBotRunner'

    def handle(self, *args, **kwargs):
        t = threading.Thread(target=init)
        t.start()
