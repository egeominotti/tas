from backtest.model.backtest import Backtest, BackTestLog

"""
Logic function
"""

from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *


def get_backtesting_hook(task):
    from backtest.models import BackTest
    print(task.result)
    print(task.result)
    print(task.result)
    if isinstance(task.result, dict):
        # BackTest.objects.filter(id=task.result.get('id')).update(scheduled=True)
        BackTest.objects.filter(id=task.result.get('id')).delete()
        qs = BackTestLog.objects.filter(time_frame=task.result.get('time_frame'), symbol=task.result.get('symbol'))
        for k in qs:
            print(k)

    if isinstance(task.result, bool):
        BackTest.objects.filter(id=task.result.get('id')).update(error=True)


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
            'id': instance.id,
            'symbol': instance.strategy.symbol_exchange.symbol,
            'time_frame': instance.strategy.time_frame.time_frame
        }
        return item

    return False
