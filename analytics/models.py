from django.db import models
from tas.models import CommonTrait


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


class ExchangeRecord(models.Model):
    symbol = models.CharField(max_length=15, blank=False, null=False)
    tf = models.CharField(max_length=15, blank=False, null=False)
    # KLINE
    unix = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(blank=False, null=False)
    open = models.FloatField(default=0, blank=False)
    high = models.FloatField(default=0, blank=False)
    low = models.FloatField(default=0, blank=False)
    close = models.FloatField(default=0, blank=False)
    volume = models.FloatField(default=0, blank=False)
    # INDICATORS
    ema = models.JSONField(blank=False, null=False)
    macd = models.JSONField(blank=True, null=True)
    fibonacciretracement = models.JSONField(blank=True, null=True)
    bbands = models.JSONField(blank=True, null=True)
    rsi = models.JSONField(blank=True, null=True)
    stochrsi = models.JSONField(blank=True, null=True)
    atr = models.JSONField(blank=True, null=True)
    pivotpoints = models.JSONField(blank=True, null=True)
    cci = models.JSONField(blank=True, null=True)
    volatility = models.JSONField(blank=True, null=True)
    stoch = models.JSONField(blank=True, null=True)
    trix = models.JSONField(blank=True, null=True)
    ma = models.JSONField(blank=True, null=True)
    breakaway = models.JSONField(blank=True, null=True)
    hammer = models.JSONField(blank=True, null=True)
    doji = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
