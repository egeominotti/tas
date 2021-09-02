from time import sleep

import decouple
import json
import redis
from django.core.management import BaseCommand
import logging
from backtest.services.computedata import compute_data_to_store
from bot.models import ComputedData

from strategy.models import SymbolExchange, TimeFrame

logger = logging.getLogger('main')

r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)


class Command(BaseCommand):
    help = 'AsyncRunnerBot'

    def handle(self, *args, **kwargs):

        symbol_futures = SymbolExchange.objects.all().order_by('created_at')
        time_frame = TimeFrame.objects.all()

        ComputedData.objects.all().delete()
        for interval in time_frame:
            for symbol in symbol_futures:
                key = str(symbol.symbol) + "_" + str(interval) + "_" + symbol.market
                if r.exists(key):
                    klines = json.loads(r.get(key))
                    if len(klines) > 0:
                        computed_data = compute_data_to_store(klines)
                        ComputedData.objects.create(
                            key=key,
                            symbol=symbol,
                            time_frame=interval,
                            data=computed_data
                        )
