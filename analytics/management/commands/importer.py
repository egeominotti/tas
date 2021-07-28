from datetime import datetime
from time import sleep

from binance import Client
from decouple import config
from django.core.management import BaseCommand
from django.db.models import Q

from analytics.models import Importer
import logging

logger = logging.getLogger('main')
client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


class Command(BaseCommand):
    help = 'Salva tutti i dati di binance'

    def handle(self, *args, **kwargs):

        while True:
            now = datetime.now().strftime("%d %b, %Y")
            symbols = [
                'BTCUSDT', 'ETHUSDT', 'BNBUSDT'
            ]
            tf = ['5m', '15m', '30m', '1h', '2h', '4h', '8h', '12h', '1d', '3d' '1M']

            for k in symbols:
                for j in tf:
                    klines = client.get_historical_klines(k, j, '01 Aug, 2017', now)

                    for entry in klines:
                        time = entry[0] / 1000
                        open = float(entry[1])
                        high = float(entry[2])
                        low = float(entry[3])
                        close = float(entry[4])
                        volume = float(entry[5])

                        qs = Importer.objects.filter(Q(symbol=k) & Q(timestamp=datetime.fromtimestamp(time)))
                        if qs.count() == 0:
                            Importer.objects.create(
                                symbol=k,
                                tf=j,
                                unix=time,
                                timestamp=datetime.fromtimestamp(time),
                                open=open,
                                high=high,
                                low=low,
                                close=close,
                                volume=volume,
                            )

                    sleep(60)
