from django.core.management import BaseCommand
from backtest.strategy.long.Scalping import ScalpingTest
from analytics.models import ExchangeRecord
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):

        qs = ExchangeRecord.objects.filter(tf='15m')
        for k in qs:
            scalping_test = ScalpingTest()
            scalping_test.settypestrategy('LONG')
            scalping_test.setvaluecandle(k.close)
            scalping_test.setema(9, 24)
            scalping_test.setratio(1.0005)
            scalping_test.settakeprofit(1.01)
            scalping_test.setstoploss(0.95)
            scalping_test.strategy()

        for k in qs:
            scalping_test = ScalpingTest()
            scalping_test.settypestrategy('SHORT')
            scalping_test.setvaluecandle(k.close)
            scalping_test.setema(9, 24)
            scalping_test.setratio(1.0005)
            scalping_test.settakeprofit(1.01)
            scalping_test.setstoploss(0.95)
            scalping_test.strategy()
