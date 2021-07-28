from datetime import datetime

from binance import Client
from decouple import config
from django.core.management import BaseCommand
from django.db.models import Q

from analytics.models import Importer
import logging

logger = logging.getLogger('main')
client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):

        while True:

            symbols = [
                'BTCUSDT',
            ]
            tf = ['1h', '1M']

            for k in symbols:
                for j in tf:
                    now = datetime.now().strftime("%d %b, %Y")
                    klines = client.get_historical_klines(k, j, '01 Aug, 2020', now)

                    for entry in klines:
                        time = entry[0] / 10000
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
