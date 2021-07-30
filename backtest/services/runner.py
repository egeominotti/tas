from backtest.model.backtest import Backtest, BackTestLog
from backtest.models import StatisticsPortfolio

"""
Logic function
"""

from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *


def get_backtesting_hook(task):
    from backtest.models import BackTest

    if isinstance(task.result, dict):

        backtest_instance = BackTest.objects.get(id=task.result.get('id'))

        BackTest.objects.filter(id=task.result.get('id')).update(scheduled=True)
        BackTest.objects.filter(id=task.result.get('id')).delete()
        qs = BackTestLog.objects.filter(time_frame=task.result.get('time_frame'), symbol=task.result.get('symbol'))

        for k in qs:

            if BackTestLog.objects.filter(time_frame=task.result.get('time_frame'),
                                          symbol=task.result.get('symbol'),
                                          entry_candle_date__gt=k.entry_candle_date).exists():

                next_obj = BackTestLog.objects.filter(time_frame=task.result.get('time_frame'),
                                                      symbol=task.result.get('symbol'),
                                                      entry_candle_date__gt=k.entry_candle_date).first()

                if k.candle_stop_loss_date is not None:
                    if next_obj.entry_candle_date < k.candle_stop_loss_date:
                        BackTestLog.objects.filter(time_frame=task.result.get('time_frame'),
                                                   symbol=task.result.get('symbol'),
                                                   entry_candle_date__exact=next_obj.entry_candle_date).delete()

                if k.candle_take_profit_date is not None:
                    if next_obj.entry_candle_date < k.candle_take_profit_date:
                        BackTestLog.objects.filter(time_frame=task.result.get('time_frame'),
                                                   symbol=task.result.get('symbol'),
                                                   entry_candle_date__exact=next_obj.entry_candle_date).delete()

        qs = BackTestLog.objects.filter(time_frame=task.result.get('time_frame'), symbol=task.result.get('symbol'))

        StatisticsPortfolio.objects.create(
            backtest= backtest_instance,
            time_frame=task.result.get('time_frame'),
            entry=len(qs),
            #take_profit=int(counterTP),
            #stop_loss=int(counterSL),
            #profit_ratio=int(profit_ratio),
            #loss_ratio=loss_ratio,
        )

    if isinstance(task.result, bool):
        BackTest.objects.filter(id=task.result.get('id')).update(error=True)


def backtesting(instance):
    if instance is not None:
        bt = Backtest(
            instance=instance,
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
