from datetime import datetime

import numpy as np
from binance import Client
from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import StrategyTest, Strategy
from backtest.models import BackTest
import pandas as pd
import logging
from binance import Client
from decouple import config
import talib as ta

logger = logging.getLogger('main')


class StrategyScalpingEMA(Strategy):

    def __init__(self, symbol, timeframe, firstinterval, secondinterval, ratio):
        super().__init__()
        self.symbol = symbol
        self.timeframe = timeframe
        self.firstinterval = firstinterval
        self.secondinterval = secondinterval
        self.ratio = ratio

    def compute_data(self, klines):
        """

        :param klines: kline ottenuta da un exchange
        :return: La lista con i valori computati
        """

        time = [entry[0] / 1000 for entry in klines]
        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]
        volume = [float(entry[5]) for entry in klines]
        close_array = np.asarray(close)

        ema9 = ta.EMA(close_array, timeperiod=9)
        ema24 = ta.EMA(close_array, timeperiod=24)
        ema100 = ta.EMA(close_array, timeperiod=100)

        listItem = []
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
            listItem.append(diz)

        return listItem

    def generate_signals(self):
        klines = self.client.get_historical_klines(self.symbol, self.timeframe, self.firstinterval, self.secondinterval)
        object_list = self.compute_data(klines)

        for item in object_list:
            if item is not None:
                ratio_value = item['ema9'] / item['ema24']
                if 1 < ratio_value < self.ratio:
                    if item['close'] > item['ema100']:
                        print("genero segnale")


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):
        TAKE_PROFIT = 1.02
        STOP_LOSS = 0.98
        RATIO = 1.00005
        st = StrategyScalpingEMA('BTCUSDT', '1h', '17 Aug, 2017', '26 Jul, 2021', RATIO)
        print(st.generate_signals())

        #
        # BackTest.objects.all().delete()
        # df = pd.read_csv("backtest/file/daily.csv")
        # df.set_index('timestamp')
        #
        # dizEntry = {}
        # counterTp = 0
        # counterSl = 0
        # scalping_test = StrategyTest()
        # scalping_test.setratio(RATIO)
        # scalping_test.settakeprofit(TAKE_PROFIT)
        # scalping_test.setstoploss(STOP_LOSS)
        # scalping_test.settypestrategy('LONG')
        #
        # for k, v in df.iterrows():
        #
        #     scalping_test.setvaluecandle(v['close'])
        #     scalping_test.setema(v['ema9'], v['ema24'], v['ema100'])
        #     scalping_test.settime(v['timestamp'])
        #
        #     valueEntry = scalping_test.check_entry()
        #     if valueEntry is not None:
        #         dizEntry[v['timestamp']] = valueEntry
        #
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
