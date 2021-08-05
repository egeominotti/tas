from analytics.models import CommonTrait
from django.db import models
from django.contrib.auth.models import AbstractUser


class ExchangeList(CommonTrait):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'ExchangeList'
        verbose_name_plural = 'ExchangeList'

    def __str__(self):
        if self.name is not None:
            return str(self.name)


class User(AbstractUser):
    telegram_notifications = models.BooleanField(default=True)
    counter_bot = models.IntegerField(default=0, blank=True)


class Exchange(CommonTrait):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    exchange = models.ForeignKey(ExchangeList, on_delete=models.CASCADE, null=False, blank=False)
    api_key = models.CharField(max_length=200, blank=False, null=False)
    api_secret = models.CharField(max_length=200, blank=False, null=False)
    balance_futures = models.FloatField(default=0, blank=True)
    balance_spot = models.FloatField(default=0, blank=True)
    leverage = models.IntegerField(default=0, blank=True)
    live = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Exchange'
        verbose_name_plural = 'Exchange'

    def __str__(self):
        if self.exchange is not None:
            return str(self.exchange)
