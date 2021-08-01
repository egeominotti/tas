from analytics.models import CommonTrait
from django.contrib.auth.models import User
from django.db import models


class ExchangeList(CommonTrait):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'ExchangeList'
        verbose_name_plural = 'ExchangeList'

    def __str__(self):
        if self.name is not None:
            return str(self.name)


class Exchange(CommonTrait):
    exchange = models.ForeignKey(ExchangeList, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    api_key = models.CharField(max_length=200, blank=False, null=False)
    api_secret = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = 'Exchange'
        verbose_name_plural = 'Exchange'

    def __str__(self):
        if self.user is not None:
            return str(self.user)
