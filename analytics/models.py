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
