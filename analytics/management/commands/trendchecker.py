import json
from datetime import datetime
from time import sleep
from analytics.models import TrendChecker
from dateutil.relativedelta import relativedelta
from backtest.services.computedata import compute_data
from binance import Client
from decouple import config
from django.core.management import BaseCommand
import logging
from strategy.models import TimeFrame, SymbolExchange

from bot.services.telegram import Telegram

logger = logging.getLogger('main')
client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))

diz = {}


def save(klines_computed, symbol, time_frame):
    if not TrendChecker.objects.filter(symbol=symbol, time_frame=time_frame).exists():
        TrendChecker.objects.create(
            symbol=symbol,
            time_frame=time_frame
        )

    qs = TrendChecker.objects.filter(symbol=symbol, time_frame=time_frame)
    countLong = 0
    countShort = 0

    for item in klines_computed:

        if item['ema5'] != 'NaN' and item['ema10'] != 'NaN':
            if item['ema5'] > item['ema10']:
                countLong += 1
                print("long")
                print(symbol)

            if item['ema5'] < item['ema10']:
                countShort += 1
                print("short")
                print(symbol)
                print(time_frame)

    qs.update(
        long=countLong,
        short=countShort
    )


class Command(BaseCommand):
    help = 'Salva tutti i dati di binance'

    def handle(self, *args, **kwargs):

        # telegram = Telegram()

        while True:

            try:

                for s in SymbolExchange.objects.filter(to_import=True).order_by('created_at'):
                    for t in TimeFrame.objects.filter(to_import=True).order_by('created_at'):

                        if s.to_import and t.to_import:

                            try:
                                now = datetime.now().strftime("%d %b, %Y")
                                prev = datetime.now() - relativedelta(days=14)
                                klines = client.get_historical_klines(s.symbol, t.time_frame,
                                                                      prev.strftime("%d %b, %Y"), now)

                                if len(klines) > 0:
                                    klines_computed = compute_data(klines)
                                    save(klines_computed, s, t)
                                continue

                            except Exception as e:
                                print(str(e))

                                # start = "Errore importazione dei dati: " + str(e) + " " + str(s.symbol) + " " + str(
                                #     t.time_frame)
                                # telegram.send(start)
                                continue
                sleep(60)
                continue

            except Exception as e:
                print(str(e))
                # start = "Errore importazione dei dati: " + str(e) + " "
                # telegram.send(start)
                continue
