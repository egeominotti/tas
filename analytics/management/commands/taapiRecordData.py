from datetime import datetime
from time import sleep

from django.core.management import BaseCommand
from analytics.services.exchangeApi import Taapi
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Registra i dati di taapi'

    def handle(self, *args, **kwargs):
        ticker = 'BTC/USDT'

        taapi = Taapi(ticker)

        emaList = []
        tfCandle = ['1m', '15m', '30m', '1h', '4h', '1d', '1w']
        for k in range(1,60):
            emaList.append(k)

        while True:

            now = datetime.now()

            if now.minute == 1:
                candle = taapi.candle('1m')
                print(candle)
                dizema = {}
                for j in emaList:
                    ema = taapi.ema(j, '1m')
                    dizema[j] = ema
                    sleep(0.1)
                    print(dizema)

            if now.minute == 15:
                candle = taapi.candle('15m')
                print(candle)
                dizema = {}
                for j in emaList:
                    ema = taapi.ema(j, '15m')
                    dizema[j] = ema
                    sleep(1)
                    print(dizema)

            sleep(1)
