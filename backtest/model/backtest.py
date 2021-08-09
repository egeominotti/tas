import pandas
from backtest.models import BackTestLog, StatisticsPortfolio
from backtest.services.computedata import compute_data
from binance import Client
from bot.models import UserExchange
from datetime import datetime
from backtest.strategy.logic.logic_function import *


class BackTesting:

    def __init__(
            self,
            instance,
            start_period,
            end_period,
    ):
        self.instance = instance
        self.start_period = start_period.strftime("%d %b,%Y")
        self.end_period = end_period.strftime("%d %b,%Y")
        self.initial_investment = instance.initial_investment
        self.symbol = instance.strategy.symbol_exchange.symbol
        self.time_frame = instance.strategy.time_frame.time_frame
        self.logic_entry = eval(instance.strategy.logic_entry.name)
        self.logic_exit = eval(instance.strategy.logic_exit.name)
        self.takeprofit = instance.strategy.logic_exit.takeprofit
        self.stoploss = instance.strategy.logic_exit.stoploss
        self.ratio = instance.strategy.logic_entry.ratio
        self.entry = None
        self.klines = None

    def run(self):

        try:
            qs = UserExchange.objects.get(user__username='egeo')
            client = Client(qs.api_key, qs.api_secret)

            self.klines = client.get_historical_klines(self.symbol, self.time_frame, self.start_period, self.end_period)
            if len(self.klines) > 0:
                self.find_entry()
                self.find_exit()

        except Exception as e:
            print(e)

    def find_entry(
            self,
    ) -> None:

        print("find entry")
        diz = {}
        computed_data = compute_data(self.klines)
        for item in computed_data:
            if item is not None:
                item['ratio'] = self.ratio
                item['time_frame'] = self.time_frame
                item['symbol'] = self.symbol
                val = self.logic_entry(item)
                if val is True:
                    diz[item['timestamp']] = item

        self.entry = diz

    def find_exit(
            self,
    ) -> None:

        # # # Erase db record
        # qsBacktest = BackTestLog.objects.filter(backtest=self.instance)
        # if qsBacktest.exists():
        #     qsBacktest.delete()
        #
        # qsPortfolio = StatisticsPortfolio.objects.filter(backtest=self.instance)
        # if qsPortfolio.exists():
        #     qsPortfolio.delete()

        computed_bars = compute_data(self.klines)
        computed_bars_dataframe = pandas.DataFrame.from_dict(computed_bars)

        for k, v in self.entry.items():

            entry_candle = v['close']
            entry_candle_timestamp = v['timestamp']

            tf = computed_bars_dataframe.loc[computed_bars_dataframe['timestamp'] > entry_candle_timestamp]

            for j, n in tf.iterrows():

                current_candle = n['close']
                currente_candle_timestamp = n['timestamp']

                percentage = (current_candle - entry_candle) / entry_candle

                item = {
                    'time_frame': self.time_frame,
                    'symbol': self.symbol,
                    'stop_loss': self.stoploss,
                    'take_profit': self.takeprofit,
                    'open_candle': entry_candle,
                    'close_candle': current_candle,
                    'stoploss_func': False,
                    'takeprofit_func': False
                }

                if self.logic_exit(item) is True:

                    if item.get('stoploss_func'):

                        BackTestLog.objects.create(
                            backtest=self.instance,
                            symbol=self.symbol,
                            time_frame=self.tf,
                            entry_candle=entry_candle,
                            entry_candle_date=entry_candle_timestamp,
                            candle_stop_loss=current_candle,
                            candle_stop_loss_date=currente_candle_timestamp,
                            stop_loss=True,
                            profit_loss=percentage,
                        )
                        break

                    if item.get('takeprofit_func'):

                        BackTestLog.objects.create(
                            backtest=self.instance,
                            symbol=self.symbol,
                            time_frame=self.time_frame,
                            entry_candle=entry_candle,
                            entry_candle_date=entry_candle_timestamp,
                            candle_take_profit=current_candle,
                            candle_take_profit_date=currente_candle_timestamp,
                            take_profit=True,
                            profit_loss=percentage,
                        )
                        break


def get_backtesting_hook(task):
    """
    DATA ANALYSIS BACKTESTING
    """
    from backtest.models import BackTest

    if isinstance(task.result, dict):

        backtest_instance = BackTest.objects.get(id=task.result.get('id'))

        BackTest.objects.filter(id=task.result.get('id')).update(scheduled=True)
        qs = BackTestLog.objects.filter(time_frame=task.result.get('time_frame'), symbol=task.result.get('symbol'))

        sum_loss = 0
        sum_takeprofit = 0
        for k in qs:

            if k.candle_stop_loss_date is not None:
                loss_percentage = (k.candle_stop_loss - k.entry_candle) / k.entry_candle
                sum_loss += loss_percentage
                BackTestLog.objects.filter(id=k.id).update(
                    loss_percentage=loss_percentage * 100
                )

            if k.candle_take_profit_date is not None:
                profit_percentage = (k.candle_take_profit - k.entry_candle) / k.entry_candle
                sum_takeprofit += profit_percentage
                BackTestLog.objects.filter(id=k.id).update(
                    profit_percentage=profit_percentage * 100
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

        sum_loss = 0
        sum_profit = 0
        counter_stoploss = 0
        counter_takeprofit = 0
        sum_composite_loss = 0
        sum_composite_profit = 0

        for k in qs:

            if k.stop_loss is True:
                counter_stoploss += 1
                # loss_value = (k.entry_candle - k.candle_stop_loss) / k.entry_candle
                # sum_composite_loss += loss_value
                # sum_loss += initial_investment * loss_value
                # initial_investment = initial_investment * loss_value

            if k.take_profit is True:
                counter_takeprofit += 1
                # profit_value = (k.entry_candle - k.take_profit) / k.entry_candle
                # sum_composite_profit += profit_value
                # sum_profit += initial_investment * profit_value
                # initial_investment = initial_investment * profit_value

        # net_profit = ((sum_loss + sum_profit) / initial_investment) * 100
        # composite_value = sum_composite_loss + sum_composite_profit

        initial_investment = backtest_instance.initial_investment
        total = sum_takeprofit - sum_loss

        sd = initial_investment + (total * initial_investment)

        StatisticsPortfolio.objects.create(
            backtest=backtest_instance,
            time_frame=task.result.get('time_frame'),
            entry=len(qs),
            take_profit=counter_takeprofit,
            stop_loss=counter_stoploss,
            initial_investment=backtest_instance.initial_investment,
            current_wallet=sd,
            composite_value=sd - initial_investment
        )

    if isinstance(task.result, bool):
        BackTest.objects.filter(id=task.result.get('id')).update(error=True)
