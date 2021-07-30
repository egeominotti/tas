from backtest.model.backtest import Backtest

"""
Logic function
"""

from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *


def get_backtesting_hook(task):
    print(task.result)
    print("HO FINITO")
    print("HO FINITO")
    print("HO FINITO")
    print("HO FINITO")


def backtesting(instance):
    print(instance.start_period.strftime("%d %b, %Y"))
    bt = Backtest(
        first_period=instance.start_period.strftime("%d %b,%Y"),
        logic_entry=eval(instance.strategy.logic_entry.name),
        logic_stoploss=eval(instance.strategy.logic_stoploss.name),
        logic_takeprofit=eval(instance.strategy.logic_takeprofit.name),
        time_frame=instance.strategy.time_frame.time_frame,
        symbol=instance.strategy.symbol_exchange.symbol,
        take_profit_value=instance.strategy.take_profit,
        stop_loss_value=instance.strategy.stop_loss,
        ratio_value=instance.strategy.ratio,
    )
    bt.run()
