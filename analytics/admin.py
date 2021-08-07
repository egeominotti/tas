from django.contrib import admin
from analytics.models import Importer, TrendChecker, ToImportCoins


class ExchangeRecordAdmin(admin.ModelAdmin):
    search_fields = ['symbol']
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
    list_display = ['symbol', 'created_at', 'updated_at', 'time_frame', 'long', 'trade_long', 'short', 'trade_short']
    list_per_page = 50
    ordering = ('id',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class ToImportCoinsAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    exclude = ('flgEnable',)
    list_display = ('coin', 'time_frame')
    ordering = ('id',)


admin.site.register(Importer, ExchangeRecordAdmin)
admin.site.register(ToImportCoins, ToImportCoinsAdmin)
admin.site.register(TrendChecker, TradeCheckerAdmin)
