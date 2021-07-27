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

        # crypto = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'MATICUSDT', 'BNBUSDT', 'CHZUSDT', 'VETUSDT', 'CAKEUSDT', 'AVAUSDT',
        #           'DOTUSDT', 'SOLUSDT', 'TRXUSDT', 'TFUELUSDT', 'BTTUSDT']
        # time_frame = '1h'
        #
        # for k in crypto:
        #     klines = client.get_historical_klines(k, time_frame, "17 Aug, 2017", now)
        #
        #     st = LongStrategyScalping_EMA_9_24_100(klines=klines, ratio=1.00005)
        #     signals = st.generate_signals()
        #     pf = PortfolioLongStrategyScalping_EMA_9_24_100(time_frame=time_frame, symbol=k,
        #                                                     klines=klines, signals=signals,
        #                                                     take_profit=1.021,
        #                                                     stop_loss=0.9845)
        #     pf.check_entry()

        crypto = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'MATICUSDT', 'BNBUSDT', 'CHZUSDT', 'VETUSDT', 'CAKEUSDT', 'AVAUSDT',
                  'DOTUSDT', 'SOLUSDT', 'TRXUSDT', 'TFUELUSDT', 'BTTUSDT']
        time_frame = ['4h', '8h', '12h', '1d', '3d', '1w', '1M']

        for k in crypto:
            for time in time_frame:
                print(time)
                print(time)
                print(time)
                print(time)
                klines = client.get_historical_klines(k, time, "17 Aug, 2017", now)

                st = LongStrategyScalping_EMA_9_24_100(klines=klines, ratio=1.00005)
                signals = st.generate_signals()
                pf = PortfolioLongStrategyScalping_EMA_9_24_100(time_frame=time, symbol=k,
                                                                klines=klines, signals=signals,
                                                                take_profit=1.021,
                                                                stop_loss=0.9845)
                pf.check_entry()
