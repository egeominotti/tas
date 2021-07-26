from bisect import bisect
from datetime import datetime

import numpy as np
import pandas
from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import Strategy
import logging
from binance import Client
from decouple import config
import talib as ta

logger = logging.getLogger('main')


class StrategyLongScalpingEMA(Strategy):

    def __init__(self, klines, ratio):
        super().__init__()
        self.klines = klines
        self.ratio = ratio

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
                # Non modificare la parte sottostante
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
            tf = computed_bars_dataframe.loc[computed_bars_dataframe['timestamp'] > v['timestamp']]
            for j, n in tf.iterrows():

                if self.logic_takeprofit(n['close'], v['close'], take_profit) is True:
                    counterTP += 1
                    break

                if self.logic_stop_loss(n['close'], v['close'], stop_loss) is True:
                    counterSL += 1
                    break

        print("-----------------------")
        print("ENTRY: " + str(len(signals)))
        print("TAKE PROFIT: " + str(counterTP))
        print("STOP LOSS: " + str(counterSL))

        profit_ratio = counterTP / len(signals) * 100
        loss_ratio = counterSL / len(signals) * 100

        print("PROFIT RATIO: " + str(int(profit_ratio)) + "%")
        print("LOSS RATIO: " + str(int(loss_ratio)) + "%")
        print("-----------------------")


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):
        now = datetime.now().strftime("%d %b, %Y")
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))

        klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, "17 Aug, 2017", now)

        st = StrategyLongScalpingEMA(klines=klines, ratio=1.00005)
        st.check_entry(take_profit=1.021, stop_loss=0.9845)
