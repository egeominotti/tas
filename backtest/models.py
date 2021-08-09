import uuid
from django.db import models
from django_quill.fields import QuillField
from strategy.models import TimeFrame, SymbolExchange
from analytics.models import CommonTrait


class LogicEntry(CommonTrait):
    name = models.CharField(max_length=200, blank=True)
    ratio = models.FloatField(default=0, blank=False)
    function = QuillField(blank=True)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'LogicEntry'
        verbose_name_plural = 'LogicEntry'


class LogicExit(CommonTrait):
    name = models.CharField(max_length=200, blank=True)
    takeprofit = models.FloatField(default=0, blank=False)
    stoploss = models.FloatField(default=0, blank=False)
    function = QuillField(blank=True)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'LogicExit'
        verbose_name_plural = 'LogicExit'


class BackTest(models.Model):
    name = models.CharField(max_length=200, blank=True)
    start_period = models.DateField(blank=False, null=False)
    end_period = models.DateField(blank=False, null=False)
    running = models.BooleanField(default=False)
    scheduled = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, null=False, blank=False)
    logic_entry = models.ForeignKey(LogicEntry, on_delete=models.CASCADE, null=False, blank=False)
    logic_exit = models.ForeignKey(LogicExit, on_delete=models.CASCADE, null=False, blank=False)
    symbol = models.ForeignKey(SymbolExchange, on_delete=models.CASCADE, null=False, blank=False)
    completed = models.BooleanField(default=False)
    initial_investment = models.FloatField(default=1000, blank=False, null=False)

    def save(self, *args, **kwargs):
        if len(self.name) == 0:
            self.name = 'backtesting_' + str(uuid.uuid4().hex)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.name:
            return self.name

    class Meta:
        verbose_name = 'BackTesting'
        verbose_name_plural = 'BackTesting'


class BackTestLog(models.Model):
    backtest = models.ForeignKey(BackTest, on_delete=models.CASCADE, null=False, blank=False)
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
    loss_percentage = models.FloatField(default=0, blank=True)
    profit_percentage = models.FloatField(default=0, blank=True)

    class Meta:
        verbose_name = 'BacktestLog'
        verbose_name_plural = 'BacktestLog'


class StatisticsPortfolio(CommonTrait):
    backtest = models.ForeignKey(BackTest, on_delete=models.CASCADE, null=False, blank=False)
    entry = models.IntegerField(default=0, blank=True)
    time_frame = models.CharField(max_length=10, blank=True)
    take_profit = models.IntegerField(default=0, blank=True)
    stop_loss = models.IntegerField(default=0, blank=True)
    profit_ratio = models.IntegerField(default=0, blank=True)
    loss_ratio = models.IntegerField(default=0, blank=True)
    profit_loss_percentage = models.FloatField(default=0, blank=True)
    initial_investment = models.FloatField(default=0, blank=True)
    current_wallet = models.FloatField(default=0, blank=True)
    composite_value = models.FloatField(default=0, blank=True)

    class Meta:
        verbose_name = 'StatisticsPortfolio'
        verbose_name_plural = 'StatisticsPortfolio'
