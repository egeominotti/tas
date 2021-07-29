from django.core.management import BaseCommand
from bot.model.bot import TradingBot
import logging
from bot.models import Bot
from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'RunnerBot'

    def handle(self, *args, **kwargs):
        qs = Bot.objects.all()

        bot = TradingBot(
            symbol=k.symbol_taapi,
            time_frame=k.strategy.time_frame,
            ratio=k.strategy.ratio,
            take_profit=k.strategy.take_profit,
            stop_loss=k.strategy.stop_loss,
            func_entry=eval(k.strategy.logic_entry_function),
            func_stop_loss=eval(k.strategy.logic_stoploss_function),
            func_take_profit=eval(k.strategy.logic_takeprofit_function),
        )
        bot.setexchange(k.symbol_exchange, k.quantity_investement, k.leverage)
        bot.run(k.sleep_run, k.sleep_profitloss)