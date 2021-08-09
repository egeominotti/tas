from django.core.management import BaseCommand
from backtest.models import BackTest
from backtest.model.backtest import Backtest as backtests
from threading import Thread
import logging

logger = logging.getLogger('main')



def init():
    for instance in BackTest.objects.all():
        bt = backtests(
            instance=instance,
            start_period=instance.start_period.strftime("%d %b,%Y"),
            end_period=instance.end_period.strftime("%d %b,%Y"),
        )
        return_value = bt.run()

        item = {
            'result': return_value,
            'id': instance.id,
            'symbol': instance.strategy.symbol_exchange.symbol,
            'time_frame': instance.strategy.time_frame.time_frame
        }
        print(item)


class Command(BaseCommand):
    help = 'AsyncRunnerBacktesting'

    def handle(self, *args, **kwargs):
        init()
        # thread = Thread(target=init)
        # thread.daemon = True
        # thread.start()
