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

        sentinel = False
        entry_price = 0
        long = False

        for k, v in df.iterrows():

            CANDLE_CLOSE_15MIN = v['close']

            """
            Strategy Long with loss profit
            """
            if long is False:
                EMA_24_CLOSE = v['EMA24']
                EMA_9_CLOSE = v['EMA9']
                ratio = EMA_9_CLOSE / EMA_24_CLOSE
                if 1 < ratio < 1.0005:
                    if EMA_9_CLOSE >= EMA_24_CLOSE:
                        if CANDLE_CLOSE_15MIN > EMA_9_CLOSE:
                            print("Apro condizione")
                            valueLong = CANDLE_CLOSE_15MIN
                            long = True

            if long is True:

                """
                Take profit short
                """
                if CANDLE_CLOSE_15MIN > valueLong * 1.02:
                    print("take profit")
                    valueLong = 0
                    long = False

                """
                Stop loss 
                """
                if CANDLE_CLOSE_15MIN < valueLong * 0.95:
                    print("stop loss")
                    valueLong = 0
                    long = False


            #  scalping_test = ScalpingTest()
            # scalping_test.settypestrategy('SHORT')
            # scalping_test.setvaluecandle(v['close'])
            # scalping_test.setema(v['EMA9'], v['EMA24'])
            # scalping_test.settime(v['time'])
            # scalping_test.setratio(1.0005)
            # scalping_test.settakeprofit(1.005)
            # scalping_test.setstoploss(0.95)
            #
            # sentinel = scalping_test.check_entry(sentinel)
            #
            # if sentinel is True:
            #     entry_price = v['close']
            #     print(" Prezzo di entrata: " + str(entry_price))
            #     value = v['close']
            #     take_profit = scalping_test.take_profit(value)
            #     stop_loss = scalping_test.stop_loss(value)
            #     sentinel = False
