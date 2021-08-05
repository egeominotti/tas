from django.db import models
from analytics.models import CommonTrait
from django_quill.fields import QuillField


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

    class Meta:
        verbose_name = 'SymbolTaapiApi'
        verbose_name_plural = 'SymbolTaapiApi'


class SymbolExchange(CommonTrait):
    symbol = models.CharField(max_length=20, blank=False)
    to_import = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SymbolExchange'
        verbose_name_plural = 'SymbolExchange'

    def __str__(self):
        if self.symbol is not None:
            return str(self.symbol)


class Coins(CommonTrait):
    coins_taapi = models.ForeignKey(SymbolTaapiApi, on_delete=models.CASCADE, null=False, blank=False)
    coins_exchange = models.ForeignKey(SymbolExchange, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        if self.coins_taapi is not None:
            return str(self.coins_taapi)

    class Meta:
        verbose_name = 'Coins'
        verbose_name_plural = 'Coins'


class LogicEntry(CommonTrait):
    name = models.CharField(max_length=200, blank=True)
    ratio = models.FloatField(default=0, blank=False)
    sleep = models.IntegerField(default=0, blank=False, null=False)
    function = QuillField(blank=True)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'LogicEntry'
        verbose_name_plural = 'LogicEntry'


class LogicExit(CommonTrait):
    name = models.CharField(max_length=200, blank=True)
    takeprofit_long = models.FloatField(default=0, blank=False)
    takeprofit_short = models.FloatField(default=0, blank=False)
    stoploss_long = models.FloatField(default=0, blank=False)
    stoploss_short = models.FloatField(default=0, blank=False)
    function = QuillField(blank=True)

    def __str__(self):
        if self.name is not None:
            return str(self.name)

    class Meta:
        verbose_name = 'LogicExit'
        verbose_name_plural = 'LogicExit'
