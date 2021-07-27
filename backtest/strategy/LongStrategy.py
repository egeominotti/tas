import pandas
from backtest.models import BackTest

from backtest.services.computedata import compute_data
from backtest.services.abstractclassstrategy import Strategy, Portfolio


class LongStrategyScalping_EMA_9_24_100(Strategy):

    def __init__(self, klines, ratio):
        super().__init__()

        self.klines = klines
        self.ratio = ratio

    def generate_signals(self) -> dict:
        diz = {}
        for item in compute_data(self.klines):
            if item is not None:
                self.logic_signals(item, diz)
        return diz

    def logic_signals(self, item, diz) -> None:

        """
        Scrivere la logica qui
        """
        ratio_value = item['ema9'] / item['ema24']
        if 1 < ratio_value < self.ratio:
            if item['close'] > item['ema100']:
                diz[item['timestamp']] = item
        """
        Fine logica
        """


class PortfolioLongStrategyScalping_EMA_9_24_100(Portfolio):

    def __init__(self, symbol, klines, signals, stop_loss, take_profit):
        super().__init__()
        self.symbol = symbol
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.klines, = klines,
        self.signals = signals
        self.name_class = self.__class__.__name__ + "_" + self.symbol
        BackTest.objects.filter(algorithm=self.name_class).delete()

    def logic_stop_loss(self, candle_close_entry, signal_candle_close, stop_loss):
        """
        Scrivere la logica qui
        """
        if candle_close_entry < signal_candle_close * stop_loss:
            return True
        return False

    def logic_takeprofit(self, candle_close_entry, signal_candle_close, take_profit):
        """
        Scrivere la logica qui
        """
        if candle_close_entry > signal_candle_close * take_profit:
            return True
        return False

    def check_entry(self):

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

                if self.logic_takeprofit(current_candle, entry_candle, self.take_profit) is True:
                    counterTP += 1
                    profit_percentage = (current_candle - entry_candle) / entry_candle

                    BackTest.objects.create(
                        symbol=self.symbol,
                        algorithm=self.name_class,
                        entry_candle=entry_candle,
                        entry_candle_date=entry_candle_timestamp,
                        candle_take_profit=current_candle,
                        candle_take_profit_date=currente_candle_timestamp,
                        take_profit=True,
                        profit_loss=profit_percentage,
                    )

                    break

                if self.logic_stop_loss(current_candle, entry_candle, self.stop_loss) is True:
                    counterSL += 1
                    stop_loss_percentage = (current_candle - entry_candle) / entry_candle

                    BackTest.objects.create(
                        symbol=self.symbol,
                        algorithm=self.name_class,
                        entry_candle=entry_candle,
                        entry_candle_date=entry_candle_timestamp,
                        candle_stop_loss=current_candle,
                        candle_stop_loss_date=currente_candle_timestamp,
                        stop_loss=True,
                        profit_loss=stop_loss_percentage,
                    )

                    break

        self.output(counterTP, counterSL, signals)

    def output(self, counterTP, counterSL, signals):
        ls = []
        qs = BackTest.objects.filter(algorithm=self.name_class)
        for i in qs: ls.append(i.profit_loss)

        print("-----------------------")
        print("SYMBOL: " + self.symbol)

        print("ENTRY: " + str(len(signals)))
        print("TAKE PROFIT: " + str(counterTP))
        print("STOP LOSS: " + str(counterSL))


        if counterTP > 0 and len(signals) > 0:
            profit_ratio = counterTP / len(signals) * 100
            print("PROFIT RATIO: " + str(int(profit_ratio)) + "%")

        if counterSL > 0 and len(signals) > 0:
            loss_ratio = counterSL / len(signals) * 100
            print("LOSS RATIO: " + str(int(loss_ratio)) + "%")

        print("PROFIT LOSS PERCENTAGE: " + str(round((sum(ls) * 100), 2)) + "%")
        print("-----------------------")
