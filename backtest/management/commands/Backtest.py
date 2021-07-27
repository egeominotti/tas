from datetime import datetime
from django.core.management import BaseCommand
import logging
from binance import Client
from decouple import config
from backtest.strategy.LongStrategy import LongStrategyScalping_EMA_9_24_100, PortfolioLongStrategyScalping_EMA_9_24_100

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Backtesting strategy scalping'

    def handle(self, *args, **kwargs):
        now = datetime.now().strftime("%d %b, %Y")
        client = Client(config('API_KEY_BINANCE'), config('API_SECRET_BINANCE'))

        crypto = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'MATICUSDT', 'BNBUSDT', 'CHZUSDT', 'VETUSDT', 'CAKEUSDT', 'AVAUSDT',
                  'DOTUSDT', 'SOLUSDT', 'TRXUSDT', 'TUFUELUSDT', 'BTTUSDT']

        for k in crypto:
            klines = client.get_historical_klines(k, Client.KLINE_INTERVAL_1HOUR, "17 Aug, 2017", now)

            st = LongStrategyScalping_EMA_9_24_100(klines=klines, ratio=1.00005)
            signals = st.generate_signals()
            pf = PortfolioLongStrategyScalping_EMA_9_24_100(symbol=k, klines=klines, signals=signals,
                                                            take_profit=1.021,
                                                            stop_loss=0.9845)
            pf.check_entry()
