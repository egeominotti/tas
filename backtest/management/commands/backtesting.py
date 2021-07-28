from django.core.management import BaseCommand
import logging
from backtest.model.backtest import Backtest
from backtest.strategy.long.logic_function import \
    logic_entry, \
    logic_stop_loss, \
    logic_takeprofit, \
    scalping_5m_rsi_bollinger, \
    stoploss_scalping_5m_rsi_bollinger, \
    takeprofit_scalping_5m_rsi_bollinger

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'backtesting'

    def handle(self, *args, **kwargs):

        crypto = 'ETHUSDT'
        RATIO = 1.00005
        TAKE_PROFIT = 1.021
        STOP_LOSS = 0.9845
        time_frame = '1h'

        bt = Backtest(
            first_period='17 Jun, 2020',
            logic_entry=logic_entry,
            logic_stoploss=logic_stop_loss,
            logic_takeprofit=logic_takeprofit,
            time_frame=time_frame,
            symbol=crypto,
            take_profit_value=TAKE_PROFIT,
            stop_loss_value=STOP_LOSS,
            ratio_value=RATIO
        )
        bt.run()
