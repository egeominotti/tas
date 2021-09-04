from django.core.management import BaseCommand
from backtest.models import BackTest
from backtest.model.backtest import BackTesting
from threading import Thread


def init():
    qs = BackTest.objects.filter(running=False, scheduled=False, completed=False)
    if qs.count() > 0:
        for instance in qs:

            bt = BackTesting(
                instance=instance,
                start_period=instance.start_period,
                end_period=instance.end_period,
            )

            thread = Thread(target=bt.run)
            thread.daemon = True
            thread.start()


class Command(BaseCommand):
    help = 'Async Runner Backtesting'

    def handle(self, *args, **kwargs):
        while True:
            init()
