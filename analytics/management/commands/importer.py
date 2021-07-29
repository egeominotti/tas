import json
from datetime import datetime
from time import sleep
from backtest.services.computedata import compute_data
from binance import Client
from decouple import config
from django.core.management import BaseCommand
from django.db.models import Q
from numpyencoder import NumpyEncoder
from analytics.models import Importer
import logging
from bot.models import TimeFrame, SymbolExchange

from bot.services.telegram import Telegram

logger = logging.getLogger('main')
client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


def save(klines_computed, symbol, time_frame):
    keyToRemove = ['timestamp', 'unix', 'open', 'high', 'low', 'close', 'volume']

    for item in klines_computed:

        qs = Importer.objects.filter(Q(symbol=symbol) & Q(tf=time_frame) & Q(timestamp=item['timestamp']))
        if not qs.exists():

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

    del item


class Command(BaseCommand):
    help = 'Salva tutti i dati di binance'

    def handle(self, *args, **kwargs):

        telegram = Telegram()

        while True:

            try:
                now = datetime.now().strftime("%d %b, %Y")
                klines_computed = None
                symbol = None
                time_frame = None

                for symbol in SymbolExchange.objects.all():
                    symbol = symbol
                    for time_frame in TimeFrame.objects.all().exclude(time_frame='1m'):
                        time_frame = time_frame

                        try:
                            klines = client.get_historical_klines(symbol, time_frame, '17 Aug, 2017', now)
                            klines_computed = compute_data(klines)
                        except Exception as e:
                            start = "Errore importazione dei dati: " + str(e) + " " + str(symbol) + " " + str(
                                time_frame)
                            telegram.send(start)
                            continue

                if klines_computed is not None:
                    save(klines_computed, symbol, time_frame)
                    sleep(60)
                    continue

            except Exception as e:
                start = "Errore importazione dei dati: " + str(e) + " "
                telegram.send(start)
                continue
