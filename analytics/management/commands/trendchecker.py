import json
from datetime import datetime
from time import sleep

import requests

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
URL_BYBT = 'https://fapi.bybt.com/api/futures/longShortChart?symbol='


def save(klines_computed, symbol, time_frame):
    if not TrendChecker.objects.filter(symbol=symbol, time_frame=time_frame).exists():
        TrendChecker.objects.create(
            symbol=symbol,
            time_frame=time_frame
        )

    countLong = 0
    countShort = 0
    qs = TrendChecker.objects.filter(symbol=symbol, time_frame=time_frame)
    qs.update(
        short=0,
        long=0
    )

    for item in klines_computed:

        if item['ema5'] != 'NaN' and item['ema10'] != 'NaN':

            if item['ema8'] > item['ema13'] > item['ema21'] > item['ema34']:
                countLong += 1

            elif item['ema8'] < item['ema13'] < item['ema21'] < item['ema34']:
                countShort += 1

    qs.update(
        long=countLong,
        short=countShort
    )


class Command(BaseCommand):
    help = 'Salva tutti i dati di binance'

    def handle(self, *args, **kwargs):

        # telegram = Telegram()
        daysBack = 30
        while True:

            try:

                for s in SymbolExchange.objects.filter(to_import=True).order_by('created_at'):
                    for t in TimeFrame.objects.filter(to_import=True).order_by('created_at'):

                        qs = TrendChecker.objects.filter(symbol=s, time_frame=t)
                        if s.to_import and t.to_import:

                            try:
                                now = datetime.now().strftime("%d %b, %Y")
                                prev = datetime.now() - relativedelta(days=daysBack)
                                klines = client.get_historical_klines(s.symbol, t.time_frame,
                                                                      prev.strftime("%d %b, %Y"), now)

                                if len(klines) > 0:
                                    klines_computed = compute_data(klines)
                                    save(klines_computed, s, t)

                                    for k in qs:

                                        qs.update(
                                            trade_long=False,
                                            trade_short=False,
                                        )

                                        tot = k.long - k.short
                                        if tot > 0:
                                            qs.update(
                                                trade_long=True
                                            )
                                        if tot < 0:
                                            qs.update(
                                                trade_short=True
                                            )

                                continue

                            except Exception as e:
                                print(str(e))
                                continue
                continue

            except Exception as e:
                print(str(e))
                continue
