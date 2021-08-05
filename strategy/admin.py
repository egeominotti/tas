from django.contrib import admin
from strategy.models import TimeFrame, SymbolExchange, SymbolTaapiApi, LogicEntry, LogicExit, Coins


class LogicEntryAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name', 'ratio', 'sleep',)
    exclude = ['flgEnable', ]


class LogicExitAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name', 'takeprofit_long', 'takeprofit_short', 'stoploss_long', 'stoploss_short')
    exclude = ['flgEnable', ]


class LogicTakepProfitAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name',)
    exclude = ['flgEnable', ]


class LogicStopLossAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name',)
    exclude = ['flgEnable', ]


class TimeFrameAdmin(admin.ModelAdmin):
    # search_fields = ['time_frame']
    list_per_page = 20
    ordering = ('id',)
    list_display = ('time_frame', 'to_import')
    exclude = ['flgEnable', ]


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


class CoinsAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'coins_taapi', 'coins_exchange')
    exclude = ['flgEnable', ]


admin.site.register(TimeFrame, TimeFrameAdmin)
admin.site.register(SymbolExchange, SymbolExchangeAdmin)
admin.site.register(SymbolTaapiApi, SymbolTaapiApiAmin)
admin.site.register(Coins, CoinsAdmin)
admin.site.register(LogicEntry, LogicEntryAdmin)
admin.site.register(LogicExit, LogicExitAdmin)
