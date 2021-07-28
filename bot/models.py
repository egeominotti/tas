from django.contrib.auth.models import User
from django.db import models
from analytics.models import CommonTrait
from django.conf import settings

BOT_STATUS = (
    ('DISABLED', 'DISABLED'),
    ('RUNNING', 'RUNNING'),
)


class StrategyDispatcher(CommonTrait):
    name = models.CharField(max_length=200, blank=False)
    logic_entry_function = models.CharField(max_length=200, blank=False)
    logic_takeprofit_function = models.CharField(max_length=200, blank=False)
    logic_stoploss_function = models.CharField(max_length=200, blank=False)


    def __str__(self):
        if self.name is not None:
            return str(self.name)

class BinanceAccount(CommonTrait):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    api_key = models.CharField(max_length=200, blank=False, null=False)
    api_secret = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        if self.user is not None:
            return str(self.user)


class Indicator(CommonTrait):
    indicator = models.CharField(max_length=15, blank=False)

    def __str__(self):
        if self.indicator is not None:
            return str(self.indicator)


class Bot(CommonTrait):
    name = models.CharField(max_length=100, blank=False)
    status = models.CharField(max_length=50, choices=BOT_STATUS, default=BOT_STATUS[0][0],
                              blank=False, null=False)
    symbol_taapi = models.CharField(max_length=15, blank=False)
    symbol_exchange = models.CharField(max_length=10, blank=False)
    time_frame = models.CharField(max_length=10, blank=False)
    ratio = models.FloatField(default=0, blank=False)
    take_profit = models.FloatField(default=0, blank=False)
    stop_loss = models.FloatField(default=0, blank=False)
    sleep_run = models.IntegerField(default=0, blank=True)
    sleep_profitloss = models.IntegerField(default=0, blank=True)
    # indicator = ['candle', 'rsi', 'bbands', 'ema', 'stoch']
    # ema_interval = ['10', '20', '50', '11']
    # ema_interval = models.TEX(blank=True, null=True)
    indicators = models.ManyToManyField(Indicator)
    quantity_investement = models.FloatField(default=0, blank=False)
    live = models.BooleanField(default=False)
    binance_account = models.ForeignKey(BinanceAccount, on_delete=models.SET_NULL, null=True, blank=True)
    strategy = models.ForeignKey(StrategyDispatcher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.name is not None:
            return str(self.name)
