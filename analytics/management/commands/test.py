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


def get_local_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    logger.info("get_local_time(): %s",current_time)
    return str(current_time)

def display_local_time():
    logger.info("Current time is: %s", get_local_time())
    return True

class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):
        API_KEY_LIST = [
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBpZXJyaTkzQGdtYWlsLmNvbSIsImlhdCI6MTYyNzAzNTMzNSwiZXhwIjo3OTM0MjM1MzM1fQ.m1f7RuvDmmdrTd1l8W7SSd_DVZxn9eabEjCoE8zED-Y',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVnZW9taW5vdHRpQGdtYWlsLmNvbSIsImlhdCI6MTYyODAzNTA1OCwiZXhwIjo3OTM1MjM1MDU4fQ.P6LKxJcVcZuguazTP9Ah3AHQ3l9UyfVME3YKs78F5MA'
        ]
        pp= secrets.choice(API_KEY_LIST)
        print(pp)

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
