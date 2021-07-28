from django.core.management import BaseCommand
import logging
from backtest.model.backtest import Backtest
from backtest.strategy.long.logic_function import *

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'backtesting'

    def handle(self, *args, **kwargs):

        crypto = 'BTCUSDT'
        RATIO = 1.00005
        TAKE_PROFIT = 1.021
        STOP_LOSS = 0.9845
        time_frame = '1d'

        bt = Backtest(
            first_period='17 Aug, 2017',
            logic_entry=scalping_5m_rsi_bollinger,
            logic_stoploss=stoploss_scalping_5m_rsi_bollinger,
            logic_takeprofit=takeprofit_scalping_5m_rsi_bollinger,
            time_frame=time_frame,
            symbol=crypto,
            take_profit_value=TAKE_PROFIT,
            stop_loss_value=STOP_LOSS,
            ratio_value=RATIO
        )
        bt.run()
