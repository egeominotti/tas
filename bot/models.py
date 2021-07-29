from django.contrib.auth.models import User
from django.db import models
from analytics.models import CommonTrait
from django_q.tasks import async_task

BOT_STATUS = (
    ('STOP', 'STOP'),
    ('START', 'START'),
)


class TimeFrame(CommonTrait):
    time_frame = models.CharField(max_length=10, blank=False)
    to_import = models.BooleanField(default=False)

    def __str__(self):
        if len(self.time_frame) > 0:
            if self.time_frame is not None:
                return str(self.time_frame)


class Strategy(CommonTrait):
    name = models.CharField(max_length=200, blank=False)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, null=False, blank=False)
    ratio = models.FloatField(default=0, blank=False)
    take_profit = models.FloatField(default=0, blank=False)
    stop_loss = models.FloatField(default=0, blank=False)
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


class SymbolTaapiApi(CommonTrait):
    symbol = models.CharField(max_length=20, blank=False)

    def __str__(self):
        if self.symbol is not None:
            return str(self.symbol)


class SymbolExchange(CommonTrait):
    symbol = models.CharField(max_length=20, blank=False)
    to_import = models.BooleanField(default=False)

    def __str__(self):
        if self.symbol is not None:
            return str(self.symbol)


class BotLogger(CommonTrait):
    entry_candle = models.FloatField(default=0, blank=True)
    stop_loss = models.BooleanField(default=False, blank=True)
    take_profit = models.BooleanField(default=False, blank=True)
    candle_stop_loss = models.FloatField(default=0, blank=True)
    candle_take_profit = models.FloatField(default=0, blank=True)
    entry_candle_date = models.DateTimeField(blank=True, null=True)
    candle_stop_loss_date = models.DateTimeField(blank=True, null=True)
    candle_take_profit_date = models.DateTimeField(blank=True, null=True)
    bot = models.ForeignKey('Bot', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.bot is not None:
            return str(self.bot.name)


class Bot(CommonTrait):
    name = models.CharField(max_length=100, blank=False)
    status = models.CharField(max_length=50, choices=BOT_STATUS, default=BOT_STATUS[0][0],
                              blank=False, null=False)

    symbol_taapi = models.ForeignKey(SymbolTaapiApi, on_delete=models.SET_NULL, null=True, blank=True)
    symbol_exchange = models.ForeignKey(SymbolExchange, on_delete=models.SET_NULL, null=True, blank=True)

    sleep_run = models.IntegerField(default=0, blank=True)
    sleep_profitloss = models.IntegerField(default=0, blank=True)
    quantity_investment = models.FloatField(default=0, blank=False)
    leverage = models.IntegerField(default=0, blank=False)
    live = models.BooleanField(default=False)
    binance_account = models.ForeignKey(BinanceAccount, on_delete=models.SET_NULL, null=True, blank=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True, blank=True)
    execution = models.BooleanField(default=False)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status == 'START':
            async_task("bot.services.runner.runnerbot", self, Bot, BotLogger)
