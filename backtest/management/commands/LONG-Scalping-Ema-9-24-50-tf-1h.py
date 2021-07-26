from datetime import datetime
from django.core.management import BaseCommand
import logging
from binance import Client
from decouple import config
from strategy.long.Strategy import StrategyLongScalpingEMA

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):
        now = datetime.now().strftime("%d %b, %Y")
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))

        klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, "17 Aug, 2017", now)

        st = StrategyLongScalpingEMA(symbol='BTCUSDT', klines=klines, ratio=1.00005)
        st.check_entry(take_profit=1.021, stop_loss=0.9845)
