from django.db import models
from tas.models import CommonTrait
from strategy.models import TimeFrame, SymbolExchange


class ByBt(CommonTrait):
    time = models.IntegerField(default=0, blank=True)
    symbol = models.CharField(max_length=100, blank=False)
    longRateList = models.JSONField(blank=True, null=True)
    shortsRateList = models.JSONField(blank=True, null=True)
    priceList = models.JSONField(blank=True, null=True)
    longShortRateList = models.JSONField(blank=True, null=True)
    longShortRateListLast = models.FloatField(default=0, blank=True)
    dateList = models.JSONField(blank=True, null=True)
    timeType = models.JSONField(blank=True, null=True)
    avg = models.FloatField(default=0, blank=True)
    sum = models.FloatField(default=0, blank=True)
    candle = models.IntegerField(default=0, blank=True)


class Importer(CommonTrait):
    symbol = models.CharField(max_length=15, blank=False, null=False)
    tf = models.CharField(max_length=15, blank=False, null=False)
    unix = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(blank=False, null=False)
    open = models.FloatField(default=0, blank=False)
    high = models.FloatField(default=0, blank=False)
    low = models.FloatField(default=0, blank=False)
    close = models.FloatField(default=0, blank=False)
    volume = models.FloatField(default=0, blank=False)
    indicators = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Importer'
        verbose_name_plural = 'Importer'

    def __str__(self):
        return str(self.id)


class TrendChecker(CommonTrait):
    symbol = models.ForeignKey(SymbolExchange, on_delete=models.CASCADE, null=False, blank=False)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, null=False, blank=False)
    long = models.FloatField(default=0, blank=False)
    short = models.FloatField(default=0, blank=False)
    trade_long = models.BooleanField(default=False)
    trade_short = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'TrendChecker'
        verbose_name_plural = 'TrendChecker'

    def __str__(self):
        return str(self.id)
