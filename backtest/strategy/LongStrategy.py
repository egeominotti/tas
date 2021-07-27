import pandas
from backtest.models import BackTest, StatisticsPortfolio

from backtest.services.computedata import compute_data
from backtest.services.abstractclassstrategy import Strategy, Portfolio


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
        for item in compute_data(self.klines):
            if item is not None:
                val = func(item, self.ratio)
                if val is True:
                    diz[item['timestamp']] = item
        return diz


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
        self.name_class = self.__class__.__name__ + "_" + self.symbol + "_" + str(self.tf)

        self.check_entry(func_stop_loss, func_take_profit)

        # Erase db record
        qsBacktest = BackTest.objects.filter(algorithm=self.name_class)
        if qsBacktest.exists():
            qsBacktest.all().delete()

        qsPortfolio = StatisticsPortfolio.objects.filter(algorithm=self.name_class)
        if qsPortfolio.exists():
            qsPortfolio.all().delete()

    def check_entry(
            self,
            func_stop_loss,
            func_take_profit
    ) -> None:

        """

        :param func_stop_loss: Funzione di stop loss
        :param func_take_profit: Funziona di take profit
        :return: None
        """

        counterTP = 0
        counterSL = 0

        signals = self.signals
        computed_bars = compute_data(self.klines)

        computed_bars_dataframe = pandas.DataFrame(computed_bars,
                                                   columns=['unix', 'timestamp', 'open', 'high', 'low', 'close',
                                                            'volume'])

        for k, v in signals.items():

            entry_candle = v['close']
            entry_candle_timestamp = v['timestamp']

            tf = computed_bars_dataframe.loc[computed_bars_dataframe['timestamp'] > entry_candle_timestamp]

            for j, n in tf.iterrows():

                current_candle = n['close']
                currente_candle_timestamp = n['timestamp']

                percentage = (current_candle - entry_candle) / entry_candle

                if func_take_profit(current_candle, entry_candle, self.take_profit, n) is True:

                    counterTP += 1
                    BackTest.objects.create(
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

                if func_stop_loss(current_candle, entry_candle, self.stop_loss, n) is True:

                    counterSL += 1
                    BackTest.objects.create(
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

        self.output(counterTP, counterSL, signals)

    def output(
            self,
            counterTP,
            counterSL,
            signals
    ) -> None:

        ls = []
        qs = BackTest.objects.filter(algorithm=self.name_class)
        for i in qs: ls.append(i.profit_loss)

        print("-----------------------------------")
        print("SYMBOL: " + self.symbol)
        print("TIME FRAME: " + str(self.tf))
        print("ENTRY: " + str(len(signals)))
        print("TAKE PROFIT: " + str(counterTP))
        print("STOP LOSS: " + str(counterSL))

        profit_ratio = 0
        if counterTP > 0 and len(signals) > 0:
            profit_ratio = counterTP / len(signals) * 100
            print("PROFIT RATIO: " + str(int(profit_ratio)) + "%")

        loss_ratio = 0
        if counterSL > 0 and len(signals) > 0:
            loss_ratio = counterSL / len(signals) * 100
            print("LOSS RATIO: " + str(int(loss_ratio)) + "%")

        profit_loss_percentage = round((sum(ls) * 100), 2)

        print("PROFIT LOSS PERCENTAGE: " + str(profit_loss_percentage) + "%")
        print("-----------------------------------")

        StatisticsPortfolio.objects.create(
            algorithm=str(self.name_class),
            time_frame=self.tf,
            entry=len(signals),
            take_profit=int(counterTP),
            stop_loss=int(counterSL),
            profit_ratio=int(profit_ratio),
            loss_ratio=loss_ratio,
            profit_loss_percentage=profit_loss_percentage
        )
