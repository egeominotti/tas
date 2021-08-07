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
    telegram_id = models.CharField(max_length=100, blank=True, null=True)
