import pandas
from backtest.models import BackTestLog, StatisticsPortfolio
from backtest.services.computedata import compute_data
from binance import Client
from bot.models import UserExchange

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
        self.symbol = instance.symbol.symbol
        self.time_frame = instance.time_frame.time_frame
        self.logic_entry = eval(instance.logic_entry.name)
        self.logic_exit = eval(instance.logic_exit.name)
        self.takeprofit = instance.logic_exit.takeprofit
        self.stoploss = instance.logic_exit.stoploss
        self.ratio = instance.logic_entry.ratio
        self.entry = None
        self.klines = None

    def run(self):

        try:
            self.instance.scheduled = True
            self.instance.save()

            qs = UserExchange.objects.get(user__username='egeo')
            client = Client(qs.api_key, qs.api_secret)

            self.klines = client.get_historical_klines(self.symbol, self.time_frame, self.start_period, self.end_period)
            if len(self.klines) > 0:
                self.instance.running = True
                self.instance.save()

                self.find_entry()
                self.find_exit()
                self.postprocessing()

        except Exception as e:
            self.instance.error = True
            self.instance.save()
            print("Esco dal backtest errore inaspettato: " + str(e))
            exit(1)

    def find_entry(
            self,
    ) -> None:

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

        # # Erase db record
        qsBacktest = BackTestLog.objects.filter(backtest=self.instance)
        if qsBacktest.exists():
            qsBacktest.delete()

        qsPortfolio = StatisticsPortfolio.objects.filter(backtest=self.instance)
        if qsPortfolio.exists():
            qsPortfolio.delete()

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

                n['time_frame'] = self.time_frame
                n['symbol'] = self.symbol
                n['stoploss'] = self.stoploss
                n['takeprofit'] = self.takeprofit
                n['entry'] = entry_candle
                n['stoploss'] = self.stoploss
                n['stoploss_func'] = False
                n['takeprofit_func'] = False

                if self.logic_exit(n) is True:

                    if n.get('stoploss_func'):
                        BackTestLog.objects.create(
                            backtest=self.instance,
                            symbol=self.symbol,
                            time_frame=self.time_frame,
                            entry_candle=entry_candle,
                            entry_candle_date=entry_candle_timestamp,
                            candle_stop_loss=current_candle,
                            candle_stop_loss_date=currente_candle_timestamp,
                            stop_loss=True,
                            profit_loss=round(percentage, 2),
                        )
                        break

                    if n.get('takeprofit_func'):
                        BackTestLog.objects.create(
                            backtest=self.instance,
                            symbol=self.symbol,
                            time_frame=self.time_frame,
                            entry_candle=entry_candle,
                            entry_candle_date=entry_candle_timestamp,
                            candle_take_profit=current_candle,
                            candle_take_profit_date=currente_candle_timestamp,
                            take_profit=True,
                            profit_loss=round(percentage, 2),
                        )
                        break

    def postprocessing(self):

        qs = BackTestLog.objects.filter(backtest=self.instance)

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

            if BackTestLog.objects.filter(backtest=self.instance,
                                          entry_candle_date__gt=k.entry_candle_date).exists():

                next_obj = BackTestLog.objects.filter(backtest=self.instance,
                                                      entry_candle_date__gt=k.entry_candle_date).first()

                if k.candle_stop_loss_date is not None:
                    if next_obj.entry_candle_date < k.candle_stop_loss_date:
                        BackTestLog.objects.filter(backtest=self.instance,
                                                   entry_candle_date__exact=next_obj.entry_candle_date).delete()

                if k.candle_take_profit_date is not None:
                    if next_obj.entry_candle_date < k.candle_take_profit_date:
                        BackTestLog.objects.filter(backtest=self.instance,
                                                   entry_candle_date__exact=next_obj.entry_candle_date).delete()

        qs = BackTestLog.objects.filter(backtest=self.instance)

        counter_stoploss = 0
        counter_takeprofit = 0

        for k in qs:

            if k.stop_loss is True:
                counter_stoploss += 1

            if k.take_profit is True:
                counter_takeprofit += 1

        initial_investment = self.instance.initial_investment

        total = sum_takeprofit + sum_loss
        value = initial_investment + (total * initial_investment)

        StatisticsPortfolio.objects.create(
            backtest=self.instance,
            time_frame=self.time_frame,
            entry=len(qs),
            take_profit=counter_takeprofit,
            stop_loss=counter_stoploss,
            initial_investment=self.instance.initial_investment,
            current_wallet=round(value, 2),
            composite_value=round(value - initial_investment, 2),
            start_period=self.instance.start_period,
            end_period=self.instance.end_period,
            symbol=self.symbol,
            logic_entry=self.instance.logic_entry.name,
            logic_exit=self.instance.logic_entry.name
        )

        self.instance.completed = True
        self.instance.save()
