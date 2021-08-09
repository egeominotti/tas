from django.core.management import BaseCommand
from backtest.models import BackTest
from backtest.model.backtest import BackTesting
from threading import Thread
import logging

logger = logging.getLogger('main')


def init():
    for instance in BackTest.objects.filter(scheduled=False):
        bt = BackTesting(
            instance=instance,
            start_period=instance.start_period,
            end_period=instance.end_period,
        )

        thread = Thread(target=bt.run)
        thread.daemon = True
        thread.start()
        thread.join()


class Command(BaseCommand):
    help = 'AsyncRunnerBacktesting'

    def handle(self, *args, **kwargs):
        init()
