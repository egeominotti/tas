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


class Command(BaseCommand):
    help = 'Salva tutti i dati di binance'

    def handle(self, *args, **kwargs):

        telegram = Telegram()

        try:

            for s in SymbolExchange.objects.filter(to_import=True).order_by('created_at'):
                for t in TimeFrame.objects.filter(to_import=True).order_by('created_at'):
                    print(s.symbol)
                    print(t.time_frame)
                    if s.to_import and t.to_import:

                        try:
                            async_task("analytics.services.importer.save",
                                       s.symbol,
                                       t.time_frame,
                                       hook="analytics.services.importer.get_save_hook")

                        except Exception as e:
                            start = "Errore importazione dei dati: " + str(e) + " " + str(s.symbol) + " " + str(
                                t.time_frame)
                            telegram.send(start)

        except Exception as e:
            start = "Errore importazione dei dati: " + str(e) + " "
            telegram.send(start)
