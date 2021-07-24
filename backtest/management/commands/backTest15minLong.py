from django.core.management import BaseCommand
from analytics.models import ExchangeRecord
import logging

logger = logging.getLogger('main')

QUANTITY = 0.004
TAKE_PROFIT = 1.01
STOP_LOSS = 0.95


class Command(BaseCommand):
    help = 'Backtesting strategy'

    def handle(self, *args, **kwargs):

        long = False
        valueLong = 0
        countOpen = 0
        countTakeProfit = 0
        countStopLoss = 0

        qs = ExchangeRecord.objects.filter(tf='1m')
        for v in qs:
            candle_close = v.close
            """
            Strategy Long with loss profit
            """
            if long is False:
                ema24 = v.ema.get('24')
                ema9 = v.ema.get('9')
                if ema9 >= ema24:
                    if candle_close > ema9:
                        ratio = ema9 / ema24
                        if ratio < 1.0005:
                            print(v.timestamp)
                            countOpen += 1
                            valueLong = candle_close
                            long = True

            if long is True:

                """
                Take profit short
                """
                if candle_close > valueLong * TAKE_PROFIT:
                    countTakeProfit += 1
                    valueLong = 0
                    long = False

                """
                Stop loss
                """
                if candle_close < valueLong * STOP_LOSS:
                    countStopLoss += 1
                    valueLong = 0
                    long = False
