from time import sleep
import multiprocessing

from bot.models import UserExchange
from django.core.management import BaseCommand
from exchange.model.binance import BinanceHelper

import logging

logger = logging.getLogger('main')


def compute(q):
    bh = BinanceHelper(
        api_key=q.api_key,
        api_secret=q.api_secret,
        symbol='BTCUSDT',
        user=q.user,
        leverage=q.leverage,
    )

    UserExchange.objects.filter(user=q.user).update(
        balance_futures=bh.get_current_balance_futures_(),
        balance_spot=bh.spot_balance()
    )


class Command(BaseCommand):
    help = 'AsyncBotRunner'

    def handle(self, *args, **kwargs):
        while True:
            sleep(30)

            qs = UserExchange.objects.all()
            processList = []

            for k in qs:
                process = multiprocessing.Process(target=compute, name=k.user, args=(k,))
                processList.append(process)

            for p in processList:
                p.daemon = True
                p.start()
                p.join()
