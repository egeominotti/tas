from django.db import models

from analytics.models import CommonTrait


class BackTest(models.Model):
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


class TimeFrame(CommonTrait):
    time_frame = models.CharField(max_length=10, blank=False)
    to_import = models.BooleanField(default=False)

    def __str__(self):
        if len(self.time_frame) > 0:
            if self.time_frame is not None:
                return str(self.time_frame)


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


class Strategy(CommonTrait):
    name = models.CharField(max_length=200, blank=False)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, null=False, blank=False)
    ratio = models.FloatField(default=0, blank=False)
    take_profit = models.FloatField(default=0, blank=False)
    stop_loss = models.FloatField(default=0, blank=False)
    logic_entry_function = models.CharField(max_length=200, blank=False)
    logic_takeprofit_function = models.CharField(max_length=200, blank=False)
    logic_stoploss_function = models.CharField(max_length=200, blank=False)
    symbol_taapi = models.ForeignKey('SymbolTaapiApi', on_delete=models.CASCADE, null=False, blank=False)
    symbol_exchange = models.ForeignKey('SymbolExchange', on_delete=models.CASCADE, null=False, blank=False)
    sleep_run = models.IntegerField(default=0, blank=False, null=False)
    sleep_profitloss = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        if self.name is not None:
            return str(self.name)
