from django.core.management import BaseCommand
import logging
from bot.model.bot import TradingBot
from bot.models import Bot, UserExchange, StrategyBot, BotLogger

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):

        try:

            qs = StrategyBot.objects.all() \
                .select_related('logic_entry') \
                .select_related('logic_exit') \
                .select_related('time_frame') \
                .prefetch_related('coins') \
                .prefetch_related('user')

            for strategy in qs:
                for user in strategy.user.filter(username='egeo'):
                    userexchange = UserExchange.objects.get(user=user)
                    for coins in strategy.coins.all():
                        if not Bot.objects.filter(user=user, coins=coins).exists():
                            bot = Bot.objects.create(user=user, strategy=strategy, coins=coins)
                            user.counter_bot = strategy.coins.count()
                            user.save()
                            print("entro")
                            # bot = TradingBot(
                            #     current_bot=bot,
                            #     user=user,
                            #     userexchange=userexchange,
                            #     symbol=bot.strategy.time_frame.time_frame,
                            #     symbol_exchange=coins.coins_exchange.symbol,
                            #     time_frame=bot.strategy.time_frame.time_frame,
                            #     func_entry=bot.strategy.logic_entry,
                            #     func_exit=bot.strategy.logic_exit,
                            #     logger=BotLogger,
                            #     bot_object=Bot
                            # )
                            # bot.run()

        except Exception as e:
            print(e)
