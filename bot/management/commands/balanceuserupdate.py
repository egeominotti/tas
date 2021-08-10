from threading import Thread
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
        symbol='',
        user=q.user,
    )

    UserExchange.objects.filter(user=q.user).update(
        balance_futures=bh.get_current_balance_futures_(),
        balance_spot=bh.spot_balance()
    )


class Command(BaseCommand):
    help = 'Bot che scarica il bilancio di ogni utente e lo salva nel sistema ogni 15 secondi'

    def handle(self, *args, **kwargs):
        pass
        # while True:
        #
        #     try:
        #
        #         qs = UserExchange.objects.filter(exchange__name='binance')
        #         print(qs)
        #         for k in qs:
        #             thread = Thread(target=compute, name=k.user, args=(k,))
        #             thread.daemon = True
        #             thread.start()
        #             thread.join()
        #         sleep(10)
        #
        #     except Exception as e:
        #         print(e)
        #         continue
