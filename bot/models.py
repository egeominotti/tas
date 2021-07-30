from exchange.models import BinanceAccount
from django.db import models
from analytics.models import CommonTrait
from django_q.tasks import async_task
from strategy.models import Strategy
import uuid

BOT_STATUS = (
    ('STOP', 'STOP'),
    ('START', 'START'),
)


class BotLogger(CommonTrait):
    bot = models.ForeignKey('Bot', on_delete=models.CASCADE, null=False, blank=False)
    entry_candle = models.FloatField(default=0, blank=True)
    stop_loss = models.BooleanField(default=False, blank=True)
    take_profit = models.BooleanField(default=False, blank=True)
    candle_stop_loss = models.FloatField(default=0, blank=True)
    candle_take_profit = models.FloatField(default=0, blank=True)
    entry_candle_date = models.DateTimeField(blank=True, null=True)
    candle_stop_loss_date = models.DateTimeField(blank=True, null=True)
    candle_take_profit_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'BotLogger'
        verbose_name_plural = 'BotLogger'

    def __str__(self):
        if self.bot is not None:
            return str(self.bot.name)


class Bot(CommonTrait):
    name = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(max_length=50, choices=BOT_STATUS, default=BOT_STATUS[0][0], blank=False, null=False)
    quantity_investment = models.FloatField(default=0, blank=False)
    leverage = models.IntegerField(default=0, blank=False)
    live = models.BooleanField(default=False)
    binance_account = models.ForeignKey(BinanceAccount, on_delete=models.SET_NULL, null=True, blank=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, null=False, blank=False)
    execution = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Bot'
        verbose_name_plural = 'Bot'

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    def save(self, *args, **kwargs):

        self.name = 'bot_' + str(uuid.uuid4().hex)
        super().save(*args, **kwargs)

        if self.status == 'START':
            async_task("bot.services.runner.runnerbot", self, Bot, BotLogger)
