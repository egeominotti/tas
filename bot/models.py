from django.conf import settings
from django.db import models
from exchange.models import ExchangeList
from analytics.models import CommonTrait
from strategy.models import TimeFrame, LogicExit, LogicEntry, Coins, SymbolExchange
from exchange.models import User
import uuid

BOT_STATUS = (
    ('STOPPED', 'STOPPED'),
    ('RUNNING', 'RUNNING'),
)

class BufferStreamWebSocket(CommonTrait):
    symbol = models.ForeignKey(SymbolExchange, on_delete=models.SET_NULL, null=True, blank=True)
    time_frame = models.CharField(max_length=4, blank=False, null=False)
    open_candle = models.FloatField(default=0, blank=True)
    close_candle = models.FloatField(default=0, blank=True)
    high_candle = models.FloatField(default=0, blank=True)
    low_candle = models.FloatField(default=0, blank=True)
    is_closed = models.BooleanField(default=False)


class UserExchange(CommonTrait):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    exchange = models.ForeignKey(ExchangeList, on_delete=models.CASCADE, null=False, blank=False)
    api_key = models.CharField(max_length=200, blank=False, null=False)
    api_secret = models.CharField(max_length=200, blank=False, null=False)
    balance_futures = models.FloatField(default=0, blank=True)
    balance_spot = models.FloatField(default=0, blank=True)
    leverage = models.IntegerField(default=0, blank=True)
    live = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'UserExchange'
        verbose_name_plural = 'UserExchange'

    def __str__(self):
        if self.exchange is not None:
            return str(self.exchange)


class BotLogger(CommonTrait):
    bot = models.ForeignKey('Bot', on_delete=models.SET_NULL, null=True, blank=True)
    entry_candle = models.FloatField(default=0, blank=True)
    stop_loss = models.BooleanField(default=False, blank=True)
    take_profit = models.BooleanField(default=False, blank=True)
    candle_stop_loss = models.FloatField(default=0, blank=True)
    candle_take_profit = models.FloatField(default=0, blank=True)
    entry_candle_date = models.DateTimeField(blank=True, null=True)
    candle_stop_loss_date = models.DateTimeField(blank=True, null=True)
    candle_take_profit_date = models.DateTimeField(blank=True, null=True)
    start_balance = models.FloatField(default=0, blank=True)
    end_balance = models.FloatField(default=0, blank=True)
    coin_quantity = models.FloatField(default=0, blank=True)
    leverage = models.IntegerField(default=0, blank=True)

    class Meta:
        verbose_name = 'BotLogger'
        verbose_name_plural = 'BotLogger'

    def __str__(self):
        if self.bot is not None:
            return str(self.bot.name)


class StrategyBot(CommonTrait):
    name = models.CharField(max_length=200, blank=False)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, null=False, blank=False)
    logic_entry = models.ForeignKey(LogicEntry, on_delete=models.CASCADE, null=False, blank=False)
    logic_exit = models.ForeignKey(LogicExit, on_delete=models.CASCADE, null=False, blank=False)
    coins = models.ManyToManyField(Coins, null=True, blank=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'Strategy'
        verbose_name_plural = 'Strategy'


class Bot(CommonTrait):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    coins = models.ForeignKey(Coins, on_delete=models.CASCADE, null=False, blank=False)
    strategy = models.ForeignKey(StrategyBot, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'Bot'
        verbose_name_plural = 'Bot'

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    def save(self, *args, **kwargs):
        if len(self.name) == 0:
            self.name = 'bot' + str(uuid.uuid4().hex)
        super().save(*args, **kwargs)
