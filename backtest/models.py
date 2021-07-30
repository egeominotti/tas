from django.db import models
from django_q.tasks import async_task
from strategy.models import Strategy
from analytics.models import CommonTrait


class BackTestLog(models.Model):
    algorithm = models.CharField(max_length=100, blank=True)
    time_frame = models.CharField(max_length=10, blank=True)
    symbol = models.CharField(max_length=20, blank=True)
    entry_candle = models.FloatField(default=0, blank=True)
    stop_loss = models.BooleanField(default=False, blank=True)
    take_profit = models.BooleanField(default=False, blank=True)
    candle_stop_loss = models.FloatField(default=0, blank=True)
    candle_take_profit = models.FloatField(default=0, blank=True)
    entry_candle_date = models.DateTimeField(blank=True, null=True)
    candle_stop_loss_date = models.DateTimeField(blank=True, null=True)
    candle_take_profit_date = models.DateTimeField(blank=True, null=True)
    profit_loss = models.FloatField(default=0, blank=True)
    function_name_logic_entry = models.CharField(max_length=100, blank=True)


class BackTest(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, null=False, blank=False)
    start_period = models.DateField(blank=True, null=True)
    end_period = models.DateField(blank=True, null=True)
    scheduled = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        async_task("backtest.services.runner.backtesting", self, hook="backtest.services.runner.get_backtesting_hook")


class StatisticsPortfolio(CommonTrait):
    algorithm = models.CharField(max_length=100, blank=True)
    entry = models.IntegerField(default=0, blank=True)
    time_frame = models.CharField(max_length=10, blank=True)
    take_profit = models.IntegerField(default=0, blank=True)
    stop_loss = models.IntegerField(default=0, blank=True)
    profit_ratio = models.IntegerField(default=0, blank=True)
    loss_ratio = models.IntegerField(default=0, blank=True)
    profit_loss_percentage = models.FloatField(default=0, blank=True)
    function_name_take_profit = models.CharField(max_length=100, blank=True)
    function_name_stop_loss = models.CharField(max_length=100, blank=True)
