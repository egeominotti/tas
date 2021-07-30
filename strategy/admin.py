from django.contrib import admin
from strategy.models import TimeFrame, SymbolExchange, SymbolTaapiApi, Strategy, LogicEntry, LogicTakepProfit, \
    LogicStopLoss


class LogicEntryAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


class LogicTakepProfitAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


class LogicStopLossAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


class StrategyDispatcherAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'name', 'logic_entry', 'logic_takeprofit', 'logic_stoploss',)
    exclude = ['flgEnable', ]


class TimeFrameAdmin(admin.ModelAdmin):
    # search_fields = ['time_frame']
    list_per_page = 20
    ordering = ('id',)
    list_display = ('time_frame', 'to_import')
    exclude = ['flgEnable', ]

    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_add_permission(self, request, obj=None):
    #     return False


class SymbolExchangeAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'symbol', 'to_import')
    exclude = ['flgEnable', ]


class SymbolTaapiApiAmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'symbol',)
    exclude = ['flgEnable', ]


admin.site.register(TimeFrame, TimeFrameAdmin)
admin.site.register(SymbolExchange, SymbolExchangeAdmin)
admin.site.register(SymbolTaapiApi, SymbolTaapiApiAmin)
admin.site.register(Strategy, StrategyDispatcherAdmin)
admin.site.register(LogicEntry, LogicEntryAdmin)
admin.site.register(LogicTakepProfit, LogicTakepProfitAdmin)
admin.site.register(LogicStopLoss, LogicStopLossAdmin)
