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

    class Meta:
        verbose_name = 'SymbolExchange'
        verbose_name_plural = 'SymbolExchange'

    def __str__(self):
        if self.symbol is not None:
            return str(self.symbol)


class Coins(CommonTrait):
    coins_exchange = models.ForeignKey(SymbolExchange, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        if self.coins_exchange is not None:
            return str(self.coins_exchange)

    class Meta:
        verbose_name = 'Coins'
        verbose_name_plural = 'Coins'
