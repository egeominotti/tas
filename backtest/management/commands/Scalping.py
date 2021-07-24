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
        print(df)
        for k, v in df.iterrows():
            scalping_test = ScalpingTest()
            scalping_test.settypestrategy('LONG')
            scalping_test.setvaluecandle(v['close'])
            scalping_test.setema(v['EMA9'], v['EMA24'])
            scalping_test.settime(v['time'])
            scalping_test.setratio(1.0005)
            scalping_test.settakeprofit(1.01)
            scalping_test.setstoploss(0.95)

            print(scalping_test.check_entry())
