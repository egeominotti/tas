from django.contrib import admin
from bot.models import Bot, Indicator, BinanceAccount, Strategy


class BotAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'id', 'name', 'status', 'strategy', 'sleep_run', 'sleep_profitloss', 'quantity_investement', 'binance_account',
        'live')
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
admin.site.register(Strategy, StrategyDispatcherAdmin)
