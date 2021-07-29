from threading import Thread
from bot.model.bot import TradingBot
from multiprocessing import Process, Queue

"""
Logic function
"""

from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *


def runnerbot(trading_bot, logger):
    print(trading_bot)

    if trading_bot.status == 'RUNNING':
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
            binance=trading_bot.binance_account,
            logger=logger
        )
        bot.run(trading_bot.sleep_run, trading_bot.sleep_profitloss)

