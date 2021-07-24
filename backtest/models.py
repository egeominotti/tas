from django.db import models
from tas.models import CommonTrait


class BackTest(models.Model):
    algorithm = models.CharField(max_length=100, blank=True)
    entry_candle = models.FloatField(default=0, blank=True)
    entry_candle_date = models.DateTimeField(blank=True, null=True)
    counter_stop_loss = models.IntegerField(default=0, blank=True)
    counter_take_profit = models.IntegerField(default=0, blank=True)
    percentage_win = models.IntegerField(default=0, blank=True)
    percentage_loss = models.IntegerField(default=0, blank=True)

