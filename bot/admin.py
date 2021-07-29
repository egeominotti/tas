from django.contrib import admin
from bot.models import Bot, BotLogger, Indicator, BinanceAccount, Strategy, SymbolTaapiApi, SymbolExchange, TimeFrame


class SymbolExchangeAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'id', 'symbol')
    exclude = ['flgEnable', ]


class SymbolTaapiApiAmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'id', 'symbol')
    exclude = ['flgEnable', ]


class SymbolTaapiApiAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'id', 'symbol')
    exclude = ['flgEnable', ]


class BotAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'id', 'status', 'strategy', 'sleep_run', 'sleep_profitloss', 'quantity_investment', 'binance_account', 'live')
    exclude = ['flgEnable', ]


class IndicatorAdmin(admin.ModelAdmin):
    search_fields = ['indicator']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'indicator',)
    exclude = ['flgEnable', ]


class BinanceAccountAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'user', 'api_key', 'api_secret')
    exclude = ['flgEnable', ]


class StrategyDispatcherAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'name', 'logic_entry_function', 'logic_takeprofit_function', 'logic_stoploss_function',)
    exclude = ['flgEnable', ]


class TimeFrameAdmin(admin.ModelAdmin):
    # search_fields = ['time_frame']
    list_per_page = 20
    ordering = ('id',)
    list_display = ('id', 'time_frame')
    exclude = ['flgEnable', ]


class BotLoggerAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    exclude = ['flgEnable', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(BotLogger, BotLoggerAdmin)
admin.site.register(Bot, BotAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(TimeFrame, TimeFrameAdmin)
admin.site.register(SymbolExchange, SymbolExchangeAdmin)
admin.site.register(SymbolTaapiApi, SymbolTaapiApiAmin)
admin.site.register(BinanceAccount, BinanceAccountAdmin)
admin.site.register(Strategy, StrategyDispatcherAdmin)
admin.site.site_header = 'Amministrazione TAS'
