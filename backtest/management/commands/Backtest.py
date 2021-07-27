from datetime import datetime
from django.core.management import BaseCommand
import logging
from binance import Client
from decouple import config
from backtest.strategy.LongStrategy import StrategyChecker, PortfolioChecker

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):

        now = datetime.now().strftime("%d %b, %Y")
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))

        crypto = ['BTCUSDT']
        time_frame = ['1h']

        def logic_signals(item) -> bool:
            ratio_value = item['ema9'] / item['ema24']
            if item['close'] > item['ema100']:
                return True
            return False

        def logic_stop_loss(candle_close_entry, signal_candle_close, stop_loss, current_item) -> bool:
            if candle_close_entry < signal_candle_close * stop_loss:
                return True
            return False

        def logic_takeprofit(candle_close_entry, signal_candle_close, take_profit, current_item) -> bool:
            if candle_close_entry > signal_candle_close * take_profit:
                return True
            return False

        for k in crypto:
            for tf in time_frame:
                klines = client.get_historical_klines(k, tf, "17 Aug, 2020", now)

                st = StrategyChecker(klines=klines, ratio=1.00005)
                pf = PortfolioChecker(func_stop_loss=logic_stop_loss,
                                      func_take_profit=logic_takeprofit,
                                      time_frame=tf,
                                      symbol=k,
                                      klines=klines,
                                      signals=st.add_strategy(logic_signals),
                                      take_profit=1.021,
                                      stop_loss=0.9845)
