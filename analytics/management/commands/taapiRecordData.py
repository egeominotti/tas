from datetime import datetime
import schedule
from analytics.models import ExchangeRecord
from django.core.management import BaseCommand
from analytics.services.exchangeApi import Taapi
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Registra i dati di taapi'

    def handle(self, *args, **kwargs):

        ticker = 'BTC/USDT'
        taapi = Taapi(ticker)
        listema = [5, 9, 12, 24, 27, 42, 50, 60]

        def scheduledTimeFrame(tf):

            candle =                taapi.candle(tf)
            candletimestamp =       datetime.fromtimestamp(candle['timestamp'])
            candleopen =            candle['open']
            candlehigh =            candle['high']
            candlelow =             candle['low']
            candleclose =           candle['close']
            candlevolume =          candle['volume']

            dizema = {}
            for j in listema:
                ema = taapi.ema(j, tf)
                dizema[j] = ema

            ExchangeRecord.objects.create(
                symbol = ticker,
                tf = tf,
                timestamp = candletimestamp,
                open = candleopen,
                high = candlehigh,
                low = candlelow,
                close = candleclose,
                volume = candlevolume,
                ema = dizema
            )

        schedule.every(1).minutes.do(scheduledTimeFrame, tf='1m')
        schedule.every(15).minutes.do(scheduledTimeFrame, tf='15m')
        schedule.every(30).minutes.do(scheduledTimeFrame, tf='30m')
        schedule.every(1).hours.do(scheduledTimeFrame, tf='1h')
        schedule.every(4).hours.do(scheduledTimeFrame, tf='4h')
        schedule.every().day.do(scheduledTimeFrame, tf='1d')
        schedule.every().week.do(scheduledTimeFrame, tf='1w')

        while True:
            schedule.run_pending()
