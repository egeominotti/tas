from time import sleep

from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import StrategyTest
from backtest.models import BackTest
import pandas as pd
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):

        TAKE_PROFIT = 1.01
        STOP_LOSS = 0.98
        RATIO = 1.0001

        BackTest.objects.all().delete()
        df = pd.read_csv("backtest/file/BINANCE_BTCUSDT_1H.csv")
        df.set_index('time')

        dizEntry = {}
        counterTp = 0
        counterSl = 0
        scalping_test = StrategyTest()
        scalping_test.setratio(RATIO)
        scalping_test.settakeprofit(TAKE_PROFIT)
        scalping_test.setstoploss(STOP_LOSS)
        scalping_test.settypestrategy('LONG')

        for k, v in df.iterrows():

            scalping_test.setvaluecandle(v['open'])
            scalping_test.setema(v['EMA9'], v['EMA24'], v['EMA100'])
            scalping_test.settime(v['time'])

            valueEntry = scalping_test.check_entry()
            if valueEntry is not None:
                dizEntry[v['time']] = valueEntry

        for time_candle, candle_close in dizEntry.items():
            pandasTimeFrmae = df.loc[df['time'] > time_candle]
            for k, v in pandasTimeFrmae.iterrows():

                take_profit = scalping_test.take_profit(v['open'], candle_close)
                stop_loss = scalping_test.stop_loss(v['open'], candle_close)

                if take_profit is True:
                    counterTp += 1
                    BackTest.objects.create(
                        algorithm='1h_scalper',
                        entry_candle=candle_close,
                        entry_candle_date=time_candle,
                        candle_take_profit=v['open'],
                        candle_take_profit_date=v['time'],
                        take_profit=True,
                    )

                    break

                if stop_loss is True:
                    counterSl += 1

                    BackTest.objects.create(
                        algorithm='1h_scalper',
                        entry_candle=candle_close,
                        entry_candle_date=time_candle,
                        candle_stop_loss=v['open'],
                        candle_stop_loss_date=v['time'],
                        stop_loss=True,
                    )

                    break


        print("-----------------------")
        print("ENTRY: " + str(len(dizEntry)))
        print("TAKE PROFIT: " + str(counterTp))
        print("STOP LOSS: " + str(counterSl))

        profit_ratio = counterTp / len(dizEntry) * 100
        loss_ratio = counterSl / len(dizEntry) * 100

        print("PROFIT RATIO: " + str(int(profit_ratio)) + "%")
        print("LOSS RATIO: " + str(int(loss_ratio)) + "%")
        print("-----------------------")
