from django.contrib import admin
from analytics.models import ExchangeRecord


class ExchangeRecordAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_display = ['id', 'symbol', 'tf', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
    list_per_page = 50
    ordering = ('id',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(ExchangeRecord, ExchangeRecordAdmin)
