from django.core.management import BaseCommand
import logging
from backtest.models import BackTest
from backtest.model.backtest import Backtest as backtests
import datetime
from time import time, sleep
import secrets

logger = logging.getLogger('main')
import time
starttime = time.time()
from backtest.strategy.logic.logic_function import *
from bot.models import BufferStreamWebSocket

class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):
        while True:
            print(BufferStreamWebSocket.objects.filter(symbol__symbol='BTCUSDT',time_frame='1m').last().close_candle)

        # for instance in BackTest.objects.all():
        #     bt = backtests(
        #         instance=instance,
        #         first_period=instance.start_period.strftime("%d %b,%Y"),
        #         logic_entry=eval(instance.strategy.logic_entry.name),
        #         logic_exit=eval(instance.strategy.logic_exit.name),
        #         time_frame=instance.strategy.time_frame.time_frame,
        #         symbol=instance.strategy.symbol_exchange.symbol,
        #         take_profit_value=instance.strategy.logic_exit.take_profit,
        #         stop_loss_value=instance.strategy.logic_exit.stop_loss,
        #         ratio_value=instance.strategy.logic_entry.ratio,
        #     )
        #     return_value = bt.run()
        #
        #     item = {
        #         'result': return_value,
        #         'id': instance.id,
        #         'symbol': instance.strategy.symbol_exchange.symbol,
        #         'time_frame': instance.strategy.time_frame.time_frame
        #     }
        #     return item
