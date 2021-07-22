from datetime import datetime
from time import sleep
import threading
import schedule
from analytics.models import ExchangeRecord
from django.core.management import BaseCommand
from analytics.services.exchangeApi import Taapi
import logging

logger = logging.getLogger('main')


ticker = 'BTC/USDT'
taapi = Taapi(ticker)
listema = [5, 9, 10, 12, 24, 27, 42, 50, 60, 223]

def scheduledTimeFrame(tf):

    sleep(10)

    candle = taapi.candle(tf)
    candletimestamp = datetime.fromtimestamp(candle['timestamp'])
    candleopen = candle['open']
    candlehigh = candle['high']
    candlelow = candle['low']
    candleclose = candle['close']
    candlevolume = candle['volume']

    dizema = {}
    for j in listema:
        ema = taapi.ema(j, tf)
        dizema[j] = ema

    ExchangeRecord.objects.create(
        symbol=ticker,
        tf=tf,
        timestamp=candletimestamp,
        open=candleopen,
        high=candlehigh,
        low=candlelow,
        close=candleclose,
        volume=candlevolume,
        ema=dizema
    )

class Command(BaseCommand):
    help = 'Registra i dati di taapi'

    def add_arguments(self, parser):
        parser.add_argument('--tf', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        scheduledTimeFrame(kwargs['tf'][0])
