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
        for trading_bot in qs:
            print(trading_bot)
            bot = TradingBot(
                current_bot=trading_bot,
                symbol=trading_bot.symbol_taapi.symbol,
                symbol_exchange=trading_bot.symbol_exchange.symbol,
                time_frame=trading_bot.strategy.time_frame.time_frame,
                ratio=trading_bot.strategy.ratio,
                take_profit=trading_bot.strategy.take_profit,
                stop_loss=trading_bot.strategy.stop_loss,
                leverage=trading_bot.leverage,
                quantity_investment=trading_bot.quantity_investment,
                func_entry=eval(trading_bot.strategy.logic_entry_function),
                func_stop_loss=eval(trading_bot.strategy.logic_stoploss_function),
                func_take_profit=eval(trading_bot.strategy.logic_takeprofit_function),
                binance=trading_bot.binance_account
            )
            bot.run(trading_bot.sleep_run, trading_bot.sleep_profitloss)
