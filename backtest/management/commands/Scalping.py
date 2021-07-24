from time import sleep

from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import ScalpingTest
from analytics.models import ExchangeRecord
import pandas as pd
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):
        # df = pd.read_csv("backtest/file/scalping_1m.csv")
        # for k, v in df.iterrows():
        #     scalping_test = ScalpingTest()
        #     scalping_test.settypestrategy('LONG')
        #     scalping_test.setvaluecandle(v['close'])
        #     scalping_test.setema(9, 24)
        #     scalping_test.setratio(1.0005)
        #     scalping_test.settakeprofit(1.01)
        #     scalping_test.setstoploss(0.95)
        #     scalping_test.strategy()

        df = pd.read_csv("backtest/file/scalping_15min.csv")

        diz = {}
        counterTp = 0
        counterSl = 0
        scalping_test = ScalpingTest()
        scalping_test.setratio(1.0005)
        scalping_test.settakeprofit(1.005)
        scalping_test.setstoploss(0.95)
        scalping_test.settypestrategy('LONG')

        for k, v in df.iterrows():

            scalping_test.setvaluecandle(v['close'])
            scalping_test.setema(v['EMA9'], v['EMA24'])
            scalping_test.settime(v['time'])

            value = scalping_test.check_entry()
            if value is not None:
                diz[v['time']] = value

        for time_candle, candle_close_entry in diz.items():
            for k, v in df.iterrows():
                if time_candle > v['time']:
                    take_profit = scalping_test.take_profit(v['close'], candle_close_entry)
                    if take_profit is True:
                        counterTp += 1

                    stop_loss = scalping_test.stop_loss(v['close'], candle_close_entry)
                    if stop_loss is True:
                        counterSl += 1

        print(counterTp)
        print(counterSl)
