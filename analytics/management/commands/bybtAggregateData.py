from django.core.management import BaseCommand
from analytics.models import ByBt
from datetime import datetime, timedelta
import datetime
import logging

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Calcola la media degli indici per 1H,2H,4H,8H,12H,24H'

    def handle(self, *args, **kwargs):
        TimeInterval = [
            1
        ]

        symbols = [
            'BTC',
            'ETH',
            'EOS',
            'LTC',
            'XRP',
            'BSV',
            'ETC',
            'TRX',
            'LINK',
        ]

        try:
            for symbol in symbols:
                for interval in TimeInterval:
                    now = datetime.datetime.now()
                    intevalDate = now - timedelta(hours=interval)
                    print(now)
                    print(intevalDate)
                    qs = ByBt.objects.filter(symbol=symbol, created_at__range=[intevalDate, now])
                    print(str(qs.count()))
                    if qs.count() == 12 or qs.count() == 24 or qs.count() == 48 or qs.count() == 96 or qs.count() == 144 or qs.count() == 288:
                        logger.info("queryset: " + str(qs.count()))

                        sum = 0
                        for y in qs: sum += y.longShortRateListLast

                        # ByBt.objects.create(
                        #     symbol=symbol,
                        #     longShortRateListLast=sum / qs.count(),
                        #     time=interval * 60
                        # )

        except Exception as e:
            logger.error("numero di query: " + str(e))
            print("Exception: " + str(e))
