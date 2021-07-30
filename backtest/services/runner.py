from backtest.model.backtest import Backtest, BackTestLog
from backtest.models import StatisticsPortfolio

"""
Logic function
"""

from backtest.strategy.long.logic_function import *
from backtest.strategy.short.logic_function import *


def get_backtesting_hook(task):
    """
    DATA ANALYSIS BACKTESTING
    """
    from backtest.models import BackTest

    if isinstance(task.result, dict):

        backtest_instance = BackTest.objects.get(id=task.result.get('id'))

        BackTest.objects.filter(id=task.result.get('id')).update(scheduled=True)
        qs = BackTestLog.objects.filter(time_frame=task.result.get('time_frame'), symbol=task.result.get('symbol'))

        for k in qs:

            if k.candle_stop_loss_date is not None:
                loss_percentage = (k.candle_stop_loss - k.entry_candle) / k.entry_candle
                BackTestLog.objects.filter(id=k.id).update(
                    loss_percentage=loss_percentage
                )

            if k.candle_take_profit_date is not None:
                profit_percentage = (k.cande_take_profit - k.entry_candle) / k.entry_candle
                BackTestLog.objects.filter(id=k.id).update(
                    profit_percentage=profit_percentage
                )

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

        initial_investment = backtest_instance.initial_investment
        sum_loss = 0
        sum_profit = 0
        counter_stoploss = 0
        counter_takeprofit = 0
        sum_composite_loss = 0
        sum_composite_profit = 0

        for k in qs:

            if k.stop_loss is True:
                counter_stoploss += 1
                loss_value = (k.entry_candle - k.candle_stop_loss) / k.entry_candle
                sum_composite_loss += loss_value
                sum_loss += initial_investment * loss_value

            if k.take_profit is True:
                counter_takeprofit += 1
                profit_value = (k.entry_candle - k.take_profit) / k.entry_candle
                sum_composite_profit += profit_value
                sum_profit += initial_investment * profit_value

        net_profit = ((sum_loss + sum_profit) / initial_investment) * 100
        composite_value = sum_composite_loss + sum_composite_profit

        StatisticsPortfolio.objects.create(
            backtest=backtest_instance,
            time_frame=task.result.get('time_frame'),
            entry=len(qs),
            take_profit=counter_takeprofit,
            stop_loss=counter_stoploss,
            initial_investment=backtest_instance.initial_investment,
            net_profit=net_profit,
            composite_value=composite_value
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
