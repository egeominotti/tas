from backtest.model.backtest import Backtest

"""
Logic function
"""

from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *


def get_backtesting_hook(task):
    from backtest.models import BackTest
    if isinstance(task.result, dict):
        print("ok")
        BackTest.objects.filter(id=task.result.get('id')).update(scheduled=True)

    if isinstance(task.result, bool):
        print("error scheduled")


def backtesting(instance):
    if instance is not None:
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
        return_value = bt.run()

        item = {
            'result': return_value,
            'id': instance.id
        }
        return item

    return False
