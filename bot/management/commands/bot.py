from django.core.management import BaseCommand
from bot.model.bot import Bot
import logging
from bot.models import Bot

from backtest.strategy.long.logic_function import \
    logic_entry, \
    logic_stop_loss, \
    logic_takeprofit, \
    scalping_5m_rsi_bollinger, \
    stoploss_scalping_5m_rsi_bollinger, \
    takeprofit_scalping_5m_rsi_bollinger

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'bot'

    def handle(self, *args, **kwargs):

        take_profit = 1.02
        stop_loss = 0.98
        ratio = 1.0098
        symbol = 'BTC/USDT'
        time_frame = '1m'
        quantity = 0.004

        indicator = ['candle', 'rsi', 'bbands', 'ema', 'stoch']
        ema_interval = ['10', '20', '50', '11']

        bot = Bot(
            symbol=symbol,
            time_frame=time_frame,
            ratio=ratio,
            take_profit=take_profit,
            stop_loss=stop_loss,
            func_entry=scalping_5m_rsi_bollinger,
            func_stop_loss=stoploss_scalping_5m_rsi_bollinger,
            func_take_profit=takeprofit_scalping_5m_rsi_bollinger,
            indicator=indicator,
            ema_interval=ema_interval,
        )
        bot.setexchange('BTCUSDT', quantity, 1)
        bot.run(50)