from django.db import models


class CommonTrait(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    flgEnable = models.BooleanField(default=True)

    class Meta:
        abstract = True
