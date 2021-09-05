from django.db import models
from analytics.models import CommonTrait


class TimeFrame(CommonTrait):
    time_frame = models.CharField(max_length=10, blank=False)

    def __str__(self):
        if len(self.time_frame) > 0:
            if self.time_frame is not None:
                return str(self.time_frame)

    class Meta:
        verbose_name = 'TimeFrame'
        verbose_name_plural = 'TimeFrame'


class SymbolExchange(CommonTrait):
    symbol = models.CharField(max_length=20, blank=False)
    market = models.CharField(max_length=20, blank=True)
    precision = models.IntegerField(default=0, blank=True)
    quantity_precision = models.IntegerField(default=0, blank=True)
    exchange = models.CharField(max_length=15, blank=True)

    class Meta:
        verbose_name = 'SymbolExchange'
        verbose_name_plural = 'SymbolExchange'

    def __str__(self):
        if self.symbol is not None:
            return str(self.symbol)
