from analytics.models import CommonTrait
from django.contrib.auth.models import User
from django.db import models


class BinanceAccount(CommonTrait):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    api_key = models.CharField(max_length=200, blank=False, null=False)
    api_secret = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        if self.user is not None:
            return str(self.user)
