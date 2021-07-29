from bot.model.bot import TradingBot

"""
Logic function
"""

from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *


def runnerbot(instance, bot_object, logger_object):
    bot = TradingBot(
        current_bot=instance,
        symbol=instance.strategy.symbol_taapi.symbol,
        symbol_exchange=instance.strategy.symbol_exchange.symbol,
        time_frame=instance.strategy.time_frame.time_frame,
        ratio=instance.strategy.ratio,
        take_profit=instance.strategy.take_profit,
        stop_loss=instance.strategy.stop_loss,
        leverage=instance.leverage,
        quantity_investment=instance.quantity_investment,
        func_entry=eval(instance.strategy.logic_entry.name),
        func_stop_loss=eval(instance.strategy.logic_stoploss.name),
        func_take_profit=eval(instance.strategy.logic_takeprofit.name),
        binance=instance.binance_account,
        logger=logger_object,
        bot_object=bot_object
    )
    bot.run(instance.strategy.sleep_run, instance.strategy.sleep_profitloss)
