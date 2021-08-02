from django.contrib.auth.models import User

from exchange.models import Exchange
from django.db import models
from analytics.models import CommonTrait
from django_q.tasks import async_task
from strategy.models import Strategy
import uuid

BOT_STATUS = (
    ('STOPPED', 'STOPPED'),
    ('RUNNING', 'RUNNING'),
)


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

    class Meta:
        verbose_name = 'BotLogger'
        verbose_name_plural = 'BotLogger'

    def __str__(self):
        if self.bot is not None:
            return str(self.bot.name)


class Bot(CommonTrait):
    name = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, null=False, blank=False)

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
