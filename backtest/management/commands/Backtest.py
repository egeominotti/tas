from django.core.management import BaseCommand
import logging
from backtest.strategy.LongStrategy import Backtest

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Backtesting'

    def handle(self, *args, **kwargs):

        def logic_entry(item, ratio) -> bool:
            ratio_value = item['ema9'] / item['ema24']
            if 1 < ratio_value < ratio:
                if item['close'] > item['ema100']:
                    return True
            return False

        def logic_stop_loss(candle_close_entry, signal_candle_close, stop_loss, item) -> bool:
            print(item)

            if candle_close_entry < signal_candle_close * stop_loss:
                return True
            return False

        def logic_takeprofit(candle_close_entry, signal_candle_close, take_profit, item) -> bool:
            print(item)
            if candle_close_entry > signal_candle_close * take_profit:
                return True
            return False

        crypto = 'BTCUSDT'
        RATIO = 1.00005
        TAKE_PROFIT = 1.021
        STOP_LOSS = 0.9845
        time_frame = '1h'

        bt = Backtest(
            first_period='17 Jun, 2017',
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
