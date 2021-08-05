import asyncio
from time import sleep

from django.core.management import BaseCommand
import logging
from bot.model.bot import TradingBot
from bot.models import Bot, UserExchange, StrategyBot, BotLogger
from asgiref.sync import sync_to_async

logger = logging.getLogger('main')
from multiprocessing import Process
import multiprocessing

# run = True
#
#
# def handler_stop_signals(signum, frame):
#     global run
#     print("SIGNAL DI STOP")
#     # todo: devo chiudere la posizione se è aperta e cancellare il bot
#     run = False
#
#
# signal.signal(signal.SIGINT, handler_stop_signals)
# signal.signal(signal.SIGTERM, handler_stop_signals)

def asyncspawnbot(bot, user, userexchange, coins):
    print("avvio bot")
    bot = TradingBot(
        current_bot=bot,
        user=user,
        userexchange=userexchange,
        symbol=bot.strategy.time_frame.time_frame,
        symbol_exchange=coins.coins_exchange.symbol,
        time_frame=bot.strategy.time_frame.time_frame,
        func_entry=bot.strategy.logic_entry,
        func_exit=bot.strategy.logic_exit,
        logger=BotLogger,
        bot_object=Bot
    )
    bot.run()


def init():
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
                            print("avvio")
                            user.counter_bot = strategy.coins.count()
                            user.save()
                            asyncspawnbot(bot, user, userexchange, coins)

                        sleep(15)
                sleep(300)
        except Exception as e:
            print(e)
            break


class Command(BaseCommand):
    help = 'AsyncBotRunner'

    def handle(self, *args, **kwargs):
        #print("Number of cpu : ", multiprocessing.cpu_count())
        p = Process(target=init)
        p.start()
        p.join()

