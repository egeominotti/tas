import datetime

import pandas
from binance import Client
from django.core.management import BaseCommand
import logging
from analytics.models import Importer
from bot.models import BufferRecordData, UserExchange
from backtest.services.computedata import compute_data

logger = logging.getLogger('main')


def ciao():
    print("ciao")


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        qs = UserExchange.objects.get(user__username='egeo')
        client = Client(qs.api_key, qs.api_secret)

        """
            time = [entry[0] / 1000 for entry in klines]
            open = [float(entry[1]) for entry in klines]
            high = [float(entry[2]) for entry in klines]
            low = [float(entry[3]) for entry in klines]
            close = [float(entry[4]) for entry in klines]
            volume = [float(entry[5]) for entry in klines]
        """

        """"
        PAZZESCO
        """
        # klines = []
        # for k in BufferRecordData.objects.filter(symbol__symbol='BTCUSDT', time_frame='1m'):
        #     print(k)
        #     list = [int(k.unix), k.open_candle, k.high_candle, k.low_candle, k.close_candle, k.volume]
        #     klines.append(list)
        # print(klines)
        # print(compute_data(klines))

        klines = []
        for k in BufferRecordData.objects.filter(symbol__symbol='BTCUSDT', time_frame='1m'):
            list = [int(k.unix), k.open_candle, k.high_candle, k.low_candle, k.close_candle, k.volume]
            klines.append(list)
        compute_klines = compute_data(klines)

        last_klines = BufferRecordData.objects.filter(symbol__symbol='BTCUSDT', time_frame='1m').last()
        computed_bars_dataframe = pandas.DataFrame.from_dict(compute_klines)
        tf = computed_bars_dataframe.iloc[[0, -1]]
        print(tf)

        # klines = []
        # for k in Importer.objects.filter(symbol='BTCUSDT', tf='5m'):
        #     print(k)
        #     list = [k.unix, k.open, k.high, k.low, k.close, k.volume]
        #     klines.append(list)
        # print(klines)
        # print(compute_data(klines))
        # klines = client.get_historical_klines('ETHUSDT', '5m','30 minutes ago UTC')
        # print(klines)
    # for k in BufferRecordData.objects.all():
    #     print(k)
    #     compute_data_from_db(k)
