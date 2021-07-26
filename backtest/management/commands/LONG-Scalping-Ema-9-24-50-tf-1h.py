from bisect import bisect
from datetime import datetime

import numpy as np
from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import Strategy
import logging
from binance import Client
from decouple import config
import talib as ta

logger = logging.getLogger('main')


class StrategyLongScalpingEMA(Strategy):

    def __init__(self, klines):
        super().__init__()
        self.klines = klines

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

    def logic(self, item, diz) -> None:

        """
        Scrivere la logica qui
        """
        ratio_value = item['ema9'] / item['ema24']
        if 1 < ratio_value < 1.00005:
            if item['close'] > item['ema100']:
                # Non modificare la parte sottostante
                diz[item['timestamp']] = item
        """
        Fine logica
        """

    def generate_signals(self) -> dict:
        diz = {}
        for item in self.computed_data():
            if item is not None:
                self.logic(item, diz)
        return diz

    # def check_entry(self, take_profit, stop_loss) -> None:
    #
    #     computed_data = self.computed_data()
    #     signals = self.generate_signals()
    #
    #     print(len(signals))
    #     print(len(computed_data))
    #     """
    #     Scrivere la logica stop_loss o take_profit
    #     """
    #
    #     return None


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):

        TAKE_PROFIT = 1.02
        STOP_LOSS = 0.98
        RATIO = 1.00005

        now = datetime.now().strftime("%d %b, %Y")
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))

        klines = client.get_historical_klines('RVNUSDT', Client.KLINE_INTERVAL_1HOUR, "17 Aug, 2017", now)
        st = StrategyLongScalpingEMA(klines)
        signals = st.generate_signals()
        print(len(signals))
        computed_bars = st.computed_data()
        print(len(computed_bars))

        # for time_candle, candle_close in dizEntry.items():
        #     pandasTimeFrmae = df.loc[df['timestamp'] > time_candle]
        #     for k, v in pandasTimeFrmae.iterrows():
        #
        #         take_profit = scalping_test.take_profit(v['close'], candle_close)
        #         stop_loss = scalping_test.stop_loss(v['close'], candle_close)
        #
        #         if take_profit is True:
        #             counterTp += 1
        #             BackTest.objects.create(
        #                 algorithm='LONG-Scalping-Ema-9-24-50-tf-1h',
        #                 entry_candle=candle_close,
        #                 entry_candle_date=time_candle,
        #                 candle_take_profit=v['close'],
        #                 candle_take_profit_date=v['timestamp'],
        #                 take_profit=True,
        #             )
        #
        #             break
        #
        #         if stop_loss is True:
        #             counterSl += 1
        #
        #             BackTest.objects.create(
        #                 algorithm='LONG-Scalping-Ema-9-24-50-tf-1h',
        #                 entry_candle=candle_close,
        #                 entry_candle_date=time_candle,
        #                 candle_stop_loss=v['close'],
        #                 candle_stop_loss_date=v['timestamp'],
        #                 stop_loss=True,
        #             )
        #
        #             break
        #
        # print("-----------------------")
        # print("ENTRY: " + str(len(dizEntry)))
        # print("TAKE PROFIT: " + str(counterTp))
        # print("STOP LOSS: " + str(counterSl))
        #
        # profit_ratio = counterTp / len(dizEntry) * 100
        # loss_ratio = counterSl / len(dizEntry) * 100
        #
        # print("PROFIT RATIO: " + str(int(profit_ratio)) + "%")
        # print("LOSS RATIO: " + str(int(loss_ratio)) + "%")
        # print("-----------------------")
