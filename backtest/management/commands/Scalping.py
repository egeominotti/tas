from time import sleep

from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import ScalpingTest
from backtest.models import BackTest
from analytics.models import ExchangeRecord
import pandas as pd
import logging
from dateutil import parser

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):

        BackTest.objects.all().delete()
        df = pd.read_csv("backtest/file/scalping_15min.csv")
        df.set_index('time')

        dizEntry = {}
        counterTp = 0
        counterSl = 0
        counterNotCondition = 0
        scalping_test = ScalpingTest()
        scalping_test.setratio(1.0005)
        scalping_test.settakeprofit(1.005)
        scalping_test.setstoploss(0.995)
        scalping_test.settypestrategy('LONG')

        for k, v in df.iterrows():

            scalping_test.setvaluecandle(v['close'])
            scalping_test.setema(v['EMA9'], v['EMA24'])
            scalping_test.settime(v['time'])

            value = scalping_test.check_entry()
            if value is not None:
                dizEntry[v['time']] = value

        print(dizEntry)
        for time_candle, candle_close in dizEntry.items():
            pandasTimeFrmae = df.loc[df['time'] > time_candle]
            for k, v in pandasTimeFrmae.iterrows():
                take_profit = scalping_test.take_profit(v['close'], candle_close)
                stop_loss = scalping_test.stop_loss(v['close'], candle_close)

                if take_profit is True:
                    counterTp += 1
                    break

                if stop_loss is True:
                    counterSl += 1
                    break

        print("-----------------------")
        print("ENTRY: " + str(len(dizEntry)))
        print("TAKE PROFIT: " + str(counterTp))
        print("STOP LOSS: " + str(counterSl))
        print("COUNTER NOT CONDITION: " + str(counterNotCondition))
        print("-----------------------")
