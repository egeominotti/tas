import json
from datetime import datetime
from multiprocessing import Process
from threading import Thread

from backtest.services.computedata import compute_data
from binance import Client
from django.core.management import BaseCommand
from django.db.models import Q
from numpyencoder import NumpyEncoder
from analytics.models import Importer
import logging
from bot.services.telegram import Telegram
from analytics.models import ToImportCoins
from bot.models import UserExchange

logger = logging.getLogger('main')

usx = UserExchange.objects.get(user__username='egeo')
client = Client(usx.api_key, usx.api_secret)
keyToRemove = ['timestamp', 'unix', 'open', 'high', 'low', 'close', 'volume']


def save(symbol, time_frame):
    now = datetime.now().strftime("%d %b, %Y")
    klines = client.get_historical_klines(symbol, time_frame, '17 Aug, 2017', now)

    if len(klines) > 0:
        klines_computed = compute_data(klines)
        for item in klines_computed:
            print(item)
            qs = Importer.objects.filter(Q(symbol=symbol) & Q(tf=time_frame) & Q(timestamp=item['timestamp']))
            if qs.count() == 0:

                imp = Importer.objects.create(
                    symbol=symbol,
                    tf=time_frame,
                    unix=item['unix'],
                    timestamp=item['timestamp'],
                    open=item['open'],
                    high=item['high'],
                    low=item['low'],
                    close=item['close'],
                    volume=item['volume'],
                )

                for key in keyToRemove:
                    del item[key]

                Importer.objects \
                    .filter(id=imp.id) \
                    .update(
                    indicators=json.dumps(item, cls=NumpyEncoder)
                )


class Command(BaseCommand):
    help = 'Salva tutti i dati di binance'

    def handle(self, *args, **kwargs):

        telegram = Telegram()

        threads = []
        qs = ToImportCoins.objects.all()
        for k in qs:
            print(k.time_frame.time_frame)
            print(k.coin.symbol)

            try:
                thread = Thread(target=save, args=(k.coin.symbol, k.time_frame.time_frame,))
                threads.append(thread)

            except Exception as e:
                start = "Errore importazione dei dati: " + str(e) + " " + str(k.coin.symbol) + " " + str(
                    k.time_frame.time_frame)
                telegram.send(start)

        for thread in threads:
            thread.daemon = True
            thread.start()
            thread.join()
