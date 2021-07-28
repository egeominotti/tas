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


class Command(BaseCommand):
    help = 'Salva tutti i dati di binance'

    def handle(self, *args, **kwargs):

        now = datetime.now().strftime("%d %b, %Y")
        keyToRemove = ['timestamp', 'unix', 'open', 'high', 'low', 'close', 'volume']
        symbols = ['BTCUSDT']
        tf = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '8h', '12h', '1d', '3d' '1M']

        while True:
            for k in symbols:
                symbol = k
                for j in tf:
                    time_frame = j

                    try:
                        klines = client.get_historical_klines(symbol, time_frame, '17 Aug, 2017', now)
                    except Exception as e:
                        continue

                    klines_computed = compute_data(klines)
                    for item in klines_computed:

                        qs = Importer.objects.filter(Q(symbol=symbol) & Q(timestamp=item['timestamp']))
                        if not qs.exists():

                            imp = Importer.objects.create(
                                symbol=symbol,
                                tf=symbol,
                                unix=item['unix'],
                                timestamp=item['timestamp'],
                                open=item['open'],
                                high=item['high'],
                                low=item['low'],
                                close=item['close'],
                                volume=item['volume'],
                            )

                            for k in keyToRemove:
                                del item[k]

                            Importer.objects.filter(id=imp.id).update(
                                indicators=json.dumps(item, cls=NumpyEncoder)
                            )

                    #sleep(30)
            # for j in Importer.objects.all():
            #     data = json.loads(j.indicators)
            #     print(data['ema24'])
