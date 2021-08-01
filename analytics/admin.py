from django.contrib import admin
from analytics.models import Importer, TrendChecker


class ExchangeRecordAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_display = ['created_at', 'symbol', 'tf', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
    list_per_page = 50
    ordering = ('id',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class TradeCheckerAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_display = ['symbol', 'time_frame', 'long', 'trade_long', 'short', 'trade_short']
    list_per_page = 50
    ordering = ('id',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Importer, ExchangeRecordAdmin)
admin.site.register(TrendChecker, TradeCheckerAdmin)
