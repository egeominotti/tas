from django.contrib import admin
from analytics.models import ExchangeRecord


class ExchangeRecordAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_display = ['tf', 'timestamp', 'open', 'high', 'low', 'close', 'volume','ema']
    list_per_page = 20


admin.site.register(ExchangeRecord, ExchangeRecordAdmin)
