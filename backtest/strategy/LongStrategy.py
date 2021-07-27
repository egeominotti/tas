import numpy as np
import pandas
from datetime import datetime
from backtest.models import BackTest
import talib as ta
from abc import ABCMeta, abstractmethod


class Strategy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError("Should implement generate_signals()!")

    @abstractmethod
    def computed_data(self):
        raise NotImplementedError("Should implement generate_signals()!")


class LongStrategyScalping_EMA_9_24_100(Strategy):

    def __init__(self, symbol, klines, ratio):
        super().__init__()
        BackTest.objects.filter(algorithm=self.__class__.__name__).delete()
        self.klines = klines
        self.ratio = ratio
        self.symbol = symbol

    def computed_data(self) -> list:

        """
        :param klines: kline ottenuta da un exchange
        :return: La lista con i valori computati
        """

        time = [entry[0] / 1000 for entry in self.klines]
        open = [float(entry[1]) for entry in self.klines]
        high = [float(entry[2]) for entry in self.klines]
        low = [float(entry[3]) for entry in self.klines]
        close = [float(entry[4]) for entry in self.klines]
        volume = [float(entry[5]) for entry in self.klines]
        close_array = np.asarray(close)

        ema9 = ta.EMA(close_array, timeperiod=9)
        ema24 = ta.EMA(close_array, timeperiod=24)
        ema100 = ta.EMA(close_array, timeperiod=100)

        computed_data = []
        lenght = len(time)
        for i in range(lenght):
            diz = {
                'unix': time[i],
                'timestamp': datetime.fromtimestamp(time[i]),
                'open': open[i],
                'high': high[i],
                'low': low[i],
                'close': close[i],
                'volume': volume[i],
                'ema9': ema9[i],
                'ema24': ema24[i],
                'ema100': ema100[i],
            }
            computed_data.append(diz)

        return computed_data

    def generate_signals(self) -> dict:
        diz = {}
        for item in self.computed_data():
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

    def check_entry(self, take_profit, stop_loss):
        counterTP = 0
        counterSL = 0

        signals = self.generate_signals()
        computed_bars = self.computed_data()

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

                if self.logic_takeprofit(current_candle, entry_candle, take_profit) is True:

                    counterTP += 1
                    profit_percentage = (current_candle - entry_candle) / entry_candle

                    BackTest.objects.create(
                        algorithm=self.__class__.__name__,
                        entry_candle=entry_candle,
                        entry_candle_date=entry_candle_timestamp,
                        candle_take_profit=current_candle,
                        candle_take_profit_date=currente_candle_timestamp,
                        take_profit=True,
                        profit_loss=profit_percentage,
                    )

                    break

                if self.logic_stop_loss(current_candle, entry_candle, stop_loss) is True:

                    counterSL += 1
                    stop_loss_percentage = (current_candle - entry_candle) / entry_candle

                    BackTest.objects.create(
                        algorithm=self.__class__.__name__,
                        entry_candle=entry_candle,
                        entry_candle_date=entry_candle_timestamp,
                        candle_stop_loss=current_candle,
                        candle_stop_loss_date=currente_candle_timestamp,
                        stop_loss=True,
                        profit_loss=stop_loss_percentage,
                    )

                    break

        print("-----------------------")
        print("SYMBOL:" + str(self.symbol))
        print("ENTRY: " + str(len(signals)))
        print("TAKE PROFIT: " + str(counterTP))
        print("STOP LOSS: " + str(counterSL))

        profit_ratio = counterTP / len(signals) * 100
        loss_ratio = counterSL / len(signals) * 100

        print("PROFIT RATIO: " + str(int(profit_ratio)) + "%")
        print("LOSS RATIO: " + str(int(loss_ratio)) + "%")
        print("-----------------------")