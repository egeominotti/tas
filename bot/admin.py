from django.contrib import admin
from bot.models import Bot, Indicator, BinanceAccount, StrategyDispatcher


class BotAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
    'id', 'name', 'status', 'time_frame', 'ratio', 'take_profit', 'stop_loss', 'strategy', 'binance_account')
    exclude = ['flgEnable', ]


class IndicatorAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'indicator',)
    exclude = ['flgEnable', ]


class BinanceAccountAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'user', 'api_key', 'api_secret')
    exclude = ['flgEnable', ]


class StrategyDispatcherAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'name', 'logic_entry_function', 'logic_takeprofit_function', 'logic_stoploss_function',)
    exclude = ['flgEnable', ]


admin.site.register(Bot, BotAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(BinanceAccount, BinanceAccountAdmin)
admin.site.register(StrategyDispatcher, StrategyDispatcherAdmin)
