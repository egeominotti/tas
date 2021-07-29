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
        for k in qs:
            print(k)
            bot = TradingBot(
                symbol=k.symbol_taapi.symbol,
                time_frame=k.strategy.time_frame.time_frame,
                ratio=k.strategy.ratio,
                take_profit=k.strategy.take_profit,
                stop_loss=k.strategy.stop_loss,
                leverage=k.leverage,
                quantity_investement=k.quantity_investement,
                func_entry=eval(k.strategy.logic_entry_function),
                func_stop_loss=eval(k.strategy.logic_stoploss_function),
                func_take_profit=eval(k.strategy.logic_takeprofit_function),
                binance=k.binance_account
            )
            bot.run(k.sleep_run, k.sleep_profitloss)
