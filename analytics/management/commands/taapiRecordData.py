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
listema = [5, 7, 9, 10, 12, 24, 27, 42, 50, 60, 100, 200, 223, 365]


def scheduledTimeFrame(tf):
    sleep(10)

    candle = taapi.candle(tf)
    candletimestamp = datetime.fromtimestamp(candle['timestamp'])
    candleunix = candle['timestamp']
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
        unix=candleunix,
        timestamp=candletimestamp,
        open=candleopen,
        high=candlehigh,
        low=candlelow,
        close=candleclose,
        volume=candlevolume,
        # INDICATORS
        ema=dizema,
        macd=taapi.macd(tf),
        fibonacciretracement=taapi.fibonacciretracement(tf),
        bbands=taapi.bbands(tf),
        rsi=taapi.rsi(tf),
        stochrsi=taapi.stochrsi(tf),
        atr=taapi.atr(tf),
        doji=taapi.doji(tf),
        hammer=taapi.hammer(tf),
        breakaway=taapi.breakaway(tf),
        ma=taapi.ma(tf),
        trix=taapi.trix(tf),
        stoch=taapi.stoch(tf),
        volatility=taapi.volatility(tf, 50),
        cci=taapi.cci(tf),
        pivotpoints=taapi.pivotpoints(tf),
    )


class Command(BaseCommand):
    help = 'Registra i dati di taapi'

    def add_arguments(self, parser):
        parser.add_argument('--tf', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        scheduledTimeFrame(kwargs['tf'][0])
