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
    def check_entry(self, take_profit, stop_loss):
        raise NotImplementedError("Should implement generate_signals()!")


class LongStrategyScalping_EMA_9_24_100(Strategy):

    def __init__(self, symbol, klines, ratio):
        super().__init__()
        BackTest.objects.filter(algorithm=self.__class__.__name__).delete()
        self.klines = klines
        self.ratio = ratio
        self.symbol = symbol

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

        ls = []
        qs = BackTest.objects.filter(algorithm=self.__class__.__name__)
        for i in qs: ls.append(i.profit_loss)

        print("-----------------------")
        print("SYMBOL:" + str(self.symbol))
        print("ENTRY: " + str(len(signals)))
        print("TAKE PROFIT: " + str(counterTP))
        print("STOP LOSS: " + str(counterSL))

        profit_ratio = counterTP / len(signals) * 100
        loss_ratio = counterSL / len(signals) * 100

        print("PROFIT RATIO: " + str(int(profit_ratio)) + "%")
        print("LOSS RATIO: " + str(int(loss_ratio)) + "%")
        print("PROFIT LOSS PERCENTAGE: " + str(round((sum(ls) * 100), 2)) + "%")
        print("-----------------------")


def compute_data(klines):
    time = [entry[0] / 1000 for entry in klines]
    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]
    volume = [float(entry[5]) for entry in klines]

    close_array = np.asarray(close)
    low_array = np.asarray(low)
    high_array = np.asarray(high)

    ema5 = ta.EMA(close_array, timeperiod=5)
    ema7 = ta.EMA(close_array, timeperiod=7)
    ema9 = ta.EMA(close_array, timeperiod=9)
    ema10 = ta.EMA(close_array, timeperiod=10)
    ema12 = ta.EMA(close_array, timeperiod=12)
    ema24 = ta.EMA(close_array, timeperiod=24)
    ema30 = ta.EMA(close_array, timeperiod=30)
    ema42 = ta.EMA(close_array, timeperiod=42)
    ema50 = ta.EMA(close_array, timeperiod=50)
    ema60 = ta.EMA(close_array, timeperiod=60)
    ema100 = ta.EMA(close_array, timeperiod=100)
    ema200 = ta.EMA(close_array, timeperiod=200)
    ema223 = ta.EMA(close_array, timeperiod=223)
    ema365 = ta.EMA(close_array, timeperiod=365)

    rsi = ta.RSI(close_array, timeperiod=14)
    macd, macdsignal, macdhist = ta.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)
    atr = ta.ATR(high_array, low_array, close_array, timeperiod=14)
    trix = ta.TRIX(close_array, timeperiod=30)
    slowk, slowd = ta.STOCH(high_array, low_array, close_array, fastk_period=5, slowk_period=3, slowk_matype=0,
                            slowd_period=3, slowd_matype=0)
    fastk, fastd = ta.STOCHF(high_array, low_array, close_array, fastk_period=5, fastd_period=3, fastd_matype=0)
    fastk_rsi, fastd_rsi = ta.STOCHRSI(close_array, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    upperband, middleband, lowerband = ta.BBANDS(close_array, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    ma20 = ta.MA(close_array, timeperiod=20, matype=0)

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
            'ema5': ema5[i],
            'ema7': ema7[i],
            'ema9': ema9[i],
            'ema10': ema10[i],
            'ema12': ema12[i],
            'ema24': ema24[i],
            'ema30': ema30[i],
            'ema42': ema42[i],
            'ema50': ema50[i],
            'ema60': ema60[i],
            'ema100': ema100[i],
            'ema200': ema200[i],
            'ema223': ema223[i],
            'ema365': ema365[i],
            'rsi': rsi[i],
            'macd': macd[i],
            'madsignal': macdsignal[i],
            'macdhist': macdhist[i],
            'atr': atr[i],
            'trix': trix[i],
            'slowk': slowk[i],
            'slowd': slowd[i],
            'fastk': fastk[i],
            'fastd': fastd[i],
            'fastk_rsi': fastk_rsi[i],
            'fastd_rsi': fastd_rsi[i],
            'upperband': upperband[i],
            'middleband': middleband[i],
            'lowerband': lowerband[i],
            'ma20': ma20[i],

        }
        computed_data.append(diz)

    return computed_data
