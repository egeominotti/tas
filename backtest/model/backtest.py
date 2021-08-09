import pandas
from backtest.models import BackTestLog, StatisticsPortfolio
from backtest.services.computedata import compute_data
from binance import Client
from bot.models import UserExchange
from datetime import datetime
from backtest.strategy.logic.logic_function import *


class Backtest:

    def __init__(self,
                 instance,
                 start_period,
                 end_period
                 ):
        self.instance = instance
        self.initial_investment = instance.initial_investment
        self.start_period = start_period.strftime("%d %b,%Y")
        self.end_period = end_period.strftime("%d %b,%Y")
        self.symbol = instance.strategy.symbol_exchange.symbol
        self.time_frame = instance.strategy.time_frame.time_frame
        self.logic_entry = eval(instance.strategy.logic_entry.name)
        self.logic_exit = eval(instance.strategy.logic_exit.name)
        self.takeprofit = instance.strategy.logic_exit.takeprofit
        self.stoploss = instance.strategy.logic_exit.stoploss
        self.ratio = instance.strategy.logic_entry.ratio

    def run(self):

        qs = UserExchange.objects.get(user__username='egeo')
        client = Client(qs.api_key, qs.api_secret)

        try:

            klines = client.get_historical_klines(self.symbol, self.time_frame, self.start_period, self.end_period)
            print(klines)

            if len(klines) > 0:
                st = StrategyChecker(klines=klines, symbol=self.symbol, time_frame=self.time_frame, ratio=self.ratio)
                PortfolioChecker(instance=self.instance,
                                 func_exit=self.logic_exit,
                                 time_frame=self.time_frame,
                                 symbol=self.symbol,
                                 klines=klines,
                                 signals=st.add_strategy(self.logic_entry),
                                 take_profit=self.takeprofit,
                                 stop_loss=self.stoploss
                                 )

                return True

        except Exception as e:
            print(e)


class PortfolioChecker:

    def __init__(
            self,
            instance,
            func_exit,
            symbol,
            time_frame,
            klines,
            signals,
            stop_loss,
            take_profit
    ):
        super().__init__()
        self.instance = instance
        self.symbol = symbol
        self.tf = time_frame,
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.klines, = klines,
        self.signals = signals
        self.tf = ''.join(self.tf)
        self.name_class = self.__class__.__name__ + "_" + self.symbol + "_TIMEFRAME_" + str(self.tf)
        self.check_entry(func_exit)

    def check_entry(
            self,
            func_exit,
    ) -> None:

        # # Erase db record
        qsBacktest = BackTestLog.objects.filter(backtest=self.instance)
        if qsBacktest.exists():
            qsBacktest.delete()

        qsPortfolio = StatisticsPortfolio.objects.filter(backtest=self.instance)
        if qsPortfolio.exists():
            qsPortfolio.delete()

        """

        :param func_stop_loss: Funzione di stop loss
        :param func_take_profit: Funziona di take profit
        :return: None
        """

        signals = self.signals
        computed_bars = compute_data(self.klines)
        computed_bars_dataframe = pandas.DataFrame.from_dict(computed_bars)

        for k, v in signals.items():

            entry_candle = v['close']
            entry_candle_timestamp = v['timestamp']

            tf = computed_bars_dataframe.loc[computed_bars_dataframe['timestamp'] > entry_candle_timestamp]

            for j, n in tf.iterrows():

                current_candle = n['close']
                currente_candle_timestamp = n['timestamp']

                percentage = (current_candle - entry_candle) / entry_candle

                item = {
                    'time_frame': self.tf,
                    'symbol': self.symbol,
                    'stop_loss': self.stop_loss,
                    'take_profit': self.take_profit,
                    'open_candle': entry_candle,
                    'close_candle': current_candle
                }

                if func_exit(item, False) is True:
                    BackTestLog.objects.create(
                        backtest=self.instance,
                        symbol=self.symbol,
                        time_frame=self.tf,
                        entry_candle=entry_candle,
                        entry_candle_date=entry_candle_timestamp,
                        candle_take_profit=current_candle,
                        candle_take_profit_date=currente_candle_timestamp,
                        take_profit=True,
                        profit_loss=percentage,
                    )
                    break

                # if func_stop_loss(item, False) is True:
                #     BackTestLog.objects.create(
                #         backtest=self.instance,
                #         symbol=self.symbol,
                #         time_frame=self.tf,
                #         entry_candle=entry_candle,
                #         entry_candle_date=entry_candle_timestamp,
                #         candle_stop_loss=current_candle,
                #         candle_stop_loss_date=currente_candle_timestamp,
                #         stop_loss=True,
                #         profit_loss=percentage,
                #     )
                #     break


class StrategyChecker:

    def __init__(
            self,
            klines,
            symbol,
            time_frame,
            ratio
    ):
        super().__init__()
        self.klines = klines
        self.symbol = symbol
        self.time_frame = time_frame
        self.ratio = ratio

    def add_strategy(
            self,
            func
    ) -> dict:

        diz = {}
        computed_data = compute_data(self.klines)
        for item in computed_data:
            if item is not None:
                item['ratio'] = self.ratio
                item['time_frame'] = self.time_frame
                item['symbol'] = self.symbol
                val = func(item)
                if val is True:
                    diz[item['timestamp']] = item
        return diz
