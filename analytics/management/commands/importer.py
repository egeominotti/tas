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

        symbols = ['BTCUSDT']
        tf = ['5m', '15m', '30m', '1h', '2h', '4h', '8h', '12h', '1d', '3d' '1M']

        while True:

            now = datetime.now().strftime("%d %b, %Y")
            klines_computed = None
            symbol = None
            time_frame = None

            for symbol in symbols:
                symbol = symbol
                for time_frame in tf:
                    time_frame = time_frame

                    try:
                        klines = client.get_historical_klines(symbol, time_frame, '17 Aug, 2017', now)
                        klines_computed = compute_data(klines)
                    except Exception as e:
                        continue

            if klines_computed is not None:
                save(klines_computed, symbol, time_frame)
                sleep(60)
                continue
