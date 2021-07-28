from django.db import models
from analytics.models import CommonTrait


class Bot(CommonTrait):
    symbol_taapi = models.CharField(max_length=15, blank=False)
    symbol_exchange = models.CharField(max_length=10, blank=False)
    time_frame = models.CharField(max_length=10, blank=False)
    ratio = models.IntegerField(default=0, blank=True)
    take_profit = models.FloatField(default=0, blank=False)
    stop_loss = models.FloatField(default=0, blank=False)
    sleep_run = models.IntegerField(default=0, blank=True)
    sleep_profitloss = models.IntegerField(default=0, blank=True)
    # indicator = ['candle', 'rsi', 'bbands', 'ema', 'stoch']
    indicators = models.JSONField(blank=True, null=True)
    # ema_interval = ['10', '20', '50', '11']
    ema_interval = models.JSONField(blank=True, null=True)
    quantity_investement = models.IntegerField(default=0, blank=True)
    logic_entry_function = models.CharField(max_length=100, blank=False)
    logic_takeprofit_function = models.CharField(max_length=100, blank=False)
    logic_stoploss_function = models.CharField(max_length=100, blank=False)
