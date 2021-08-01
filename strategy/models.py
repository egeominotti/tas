from django.db import models
from analytics.models import CommonTrait


class TimeFrame(CommonTrait):
    time_frame = models.CharField(max_length=10, blank=False)
    to_import = models.BooleanField(default=False)

    def __str__(self):
        if len(self.time_frame) > 0:
            if self.time_frame is not None:
                return str(self.time_frame)

    class Meta:
        verbose_name = 'TimeFrame'
        verbose_name_plural = 'TimeFrame'


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


class LogicEntry(CommonTrait):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'LogicEntry'
        verbose_name_plural = 'LogicEntry'


class LogicTakepProfit(CommonTrait):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'LogicTakepProfit'
        verbose_name_plural = 'LogicTakepProfit'


class LogicStopLoss(CommonTrait):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'LogicStopLoss'
        verbose_name_plural = 'LogicStopLoss'


class Strategy(CommonTrait):
    name = models.CharField(max_length=200, blank=False)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, null=False, blank=False)
    ratio = models.FloatField(default=0, blank=False)
    take_profit = models.FloatField(default=0, blank=False)
    stop_loss = models.FloatField(default=0, blank=False)

    logic_entry = models.ForeignKey(LogicEntry, on_delete=models.CASCADE, null=False, blank=False)
    logic_takeprofit = models.ForeignKey(LogicTakepProfit, on_delete=models.CASCADE, null=False, blank=False)
    logic_stoploss = models.ForeignKey(LogicStopLoss, on_delete=models.CASCADE, null=False, blank=False)

    symbol_taapi = models.ForeignKey('SymbolTaapiApi', on_delete=models.CASCADE, null=False, blank=False)
    symbol_exchange = models.ForeignKey('SymbolExchange', on_delete=models.CASCADE, null=False, blank=False)
    sleep_run = models.IntegerField(default=0, blank=False, null=False)
    sleep_profitloss = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'Strategy'
        verbose_name_plural = 'Strategy'
