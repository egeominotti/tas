from datetime import datetime

import json
from binance import Client
from dateutil.relativedelta import relativedelta
from decouple import config
from django.db.models import Q
from numpyencoder import NumpyEncoder

from analytics.models import Importer
from backtest.services.computedata import compute_data

client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))


def get_save_hook(task):
    print(task)
    print(task.result)
    print("finito")


def save(symbol, time_frame):
    print(symbol)
    print(time_frame)
    keyToRemove = ['timestamp', 'unix', 'open', 'high', 'low', 'close', 'volume']
    now = datetime.now().strftime("%d %b, %Y")
    klines = client.get_historical_klines(symbol, time_frame, '17 Aug, 2017', now)

    if len(klines) > 0:
        klines_computed = compute_data(klines)

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
