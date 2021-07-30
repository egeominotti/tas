import pandas
from backtest.models import BackTestLog, StatisticsPortfolio
from backtest.services.computedata import compute_data
from backtest.model.portfolio import Portfolio
from backtest.model.strategy import Strategy
from binance import Client
from decouple import config
from datetime import datetime


class PortfolioChecker(Portfolio):

    def __init__(
            self,
            func_stop_loss,
            func_take_profit,
            symbol,
            time_frame,
            klines,
            signals,
            stop_loss,
            take_profit
    ):
        super().__init__()

        self.symbol = symbol
        self.tf = time_frame,
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.klines, = klines,
        self.signals = signals
        self.tf = ''.join(self.tf)
        self.name_class = self.__class__.__name__ + "_" + self.symbol + "_TIMEFRAME_" + str(self.tf)
        self.check_entry(func_stop_loss, func_take_profit)

    def check_entry(
            self,
            func_stop_loss,
            func_take_profit
    ) -> None:

        function_name_take_profit = func_stop_loss.__name__
        function_name_stop_loss = func_take_profit.__name__

        # Erase db record
        qsBacktest = BackTestLog.objects.filter(algorithm__exact=self.name_class)
        if qsBacktest.exists():
            qsBacktest.delete()

        qsPortfolio = StatisticsPortfolio.objects.filter(algorithm__exact=self.name_class)
        if qsPortfolio.exists():
            qsPortfolio.delete()

        """

        :param func_stop_loss: Funzione di stop loss
        :param func_take_profit: Funziona di take profit
        :return: None
        """

        counterTP = 0
        counterSL = 0

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

                if func_take_profit(item) is True:
                    counterTP += 1

                    BackTestLog.objects.create(
                        symbol=self.symbol,
                        time_frame=self.tf,
                        algorithm=self.name_class,
                        entry_candle=entry_candle,
                        entry_candle_date=entry_candle_timestamp,
                        candle_take_profit=current_candle,
                        candle_take_profit_date=currente_candle_timestamp,
                        take_profit=True,
                        profit_loss=percentage,
                    )
                    break

                if func_stop_loss(item) is True:
                    counterSL += 1

                    BackTestLog.objects.create(
                        symbol=self.symbol,
                        time_frame=self.tf,
                        algorithm=self.name_class,
                        entry_candle=entry_candle,
                        entry_candle_date=entry_candle_timestamp,
                        candle_stop_loss=current_candle,
                        candle_stop_loss_date=currente_candle_timestamp,
                        stop_loss=True,
                        profit_loss=percentage,
                    )

                    break

        self.output(counterTP, counterSL, signals, function_name_take_profit, function_name_stop_loss)

    def output(
            self,
            counterTP,
            counterSL,
            signals,
            function_name_take_profit,
            function_name_stop_loss

    ) -> None:

        ls = []
        qs = BackTestLog.objects.filter(algorithm=self.name_class)
        for i in qs: ls.append(i.profit_loss)

        # print("-----------------------------------")
        # print("SYMBOL: " + self.symbol)
        # print("TIME FRAME: " + str(self.tf))
        # print("ENTRY: " + str(len(signals)))
        # print("TAKE PROFIT: " + str(counterTP))
        # print("STOP LOSS: " + str(counterSL))

        profit_ratio = 0
        if counterTP > 0 and len(signals) > 0:
            profit_ratio = counterTP / len(signals) * 100
            # print("PROFIT RATIO: " + str(int(profit_ratio)) + "%")

        loss_ratio = 0
        if counterSL > 0 and len(signals) > 0:
            loss_ratio = counterSL / len(signals) * 100
            # print("LOSS RATIO: " + str(int(loss_ratio)) + "%")

        profit_loss_percentage = round((sum(ls) * 100), 2)
        #
        # print("PROFIT LOSS PERCENTAGE: " + str(profit_loss_percentage) + "%")
        # print("-----------------------------------")

        StatisticsPortfolio.objects.create(
            algorithm=str(self.name_class),
            time_frame=self.tf,
            entry=len(signals),
            take_profit=int(counterTP),
            stop_loss=int(counterSL),
            profit_ratio=int(profit_ratio),
            loss_ratio=loss_ratio,
            profit_loss_percentage=profit_loss_percentage,
            function_name_take_profit=function_name_take_profit,
            function_name_stop_loss=function_name_stop_loss,
        )


class StrategyChecker(Strategy):

    def __init__(
            self,
            klines,
            ratio
    ):
        super().__init__()
        self.klines = klines
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
                val = func(item)
                if val is True:
                    diz[item['timestamp']] = item
        return diz


class Backtest:

    def __init__(self,
                 first_period,
                 logic_entry,
                 logic_stoploss,
                 logic_takeprofit,
                 time_frame,
                 symbol,
                 take_profit_value=0,
                 stop_loss_value=0,
                 ratio_value=0
                 ):
        self.first_period = first_period
        self.logic_entry = logic_entry
        self.logic_stoploss = logic_stoploss
        self.logic_takeprofit = logic_takeprofit
        self.tf = str(time_frame),
        self.symbol = symbol
        self.take_profit_value = take_profit_value
        self.stop_loss_value = stop_loss_value
        self.ratio_value = ratio_value
        self.tf = ''.join(self.tf)

    def run(self):
        now = datetime.now().strftime("%d %b, %Y")
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))

        klines = client.get_historical_klines(self.symbol, self.tf, self.first_period, now)

        st = StrategyChecker(klines=klines, ratio=self.ratio_value)
        PortfolioChecker(func_stop_loss=self.logic_stoploss,
                         func_take_profit=self.logic_takeprofit,
                         time_frame=self.tf,
                         symbol=self.symbol,
                         klines=klines,
                         signals=st.add_strategy(self.logic_entry),
                         take_profit=self.take_profit_value,
                         stop_loss=self.stop_loss_value
                         )
        if len(klines) > 0:
            return True
