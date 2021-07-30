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
from strategy.models import TimeFrame, SymbolExchange

from bot.services.telegram import Telegram

logger = logging.getLogger('main')
client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


def save(klines_computed, symbol, time_frame):
    keyToRemove = ['timestamp', 'unix', 'open', 'high', 'low', 'close', 'volume']

    for item in klines_computed:

        qs = Importer.objects.filter(Q(symbol=symbol) & Q(tf=time_frame) & Q(timestamp=item['timestamp']))
        if len(qs) == 0:

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

        while True:

            try:

                now = datetime.now().strftime("%d %b, %Y")

                for s in SymbolExchange.objects.all():
                    for t in TimeFrame.objects.all():

                        if s.to_import and t.to_import:

                            try:

                                klines = client.get_historical_klines(s.symbol, t.time_frame, '17 Aug, 2017', now)

                                if len(klines) > 0:
                                    klines_computed = compute_data(klines)
                                    save(klines_computed, s.symbol, t.time_frame)
                                    sleep(5)

                            except Exception as e:

                                start = "Errore importazione dei dati: " + str(e) + " " + str(s.symbol) + " " + str(
                                    t.time_frame)
                                telegram.send(start)
                                continue

            except Exception as e:
                start = "Errore importazione dei dati: " + str(e) + " "
                telegram.send(start)
                continue
