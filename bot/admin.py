from django.contrib import admin
from bot.models import Bot, ClusterBot, BotLogger, StrategyBot, LogicExit, LogicEntry
from bot.models import UserExchange


class BotAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = \
        ('name',
         'user',
         'market_spot',
         'market_futures',
         'leverage',
         'amount',
         'running',
         'abort',
         'strategy',
         'coins',
         'created_at',
         )

    readonly_fields = ('name', 'running', 'abort')
    exclude = ['flgEnable', ]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class ClusterBotAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = \
        ('name',
         'user',
         'profit',
         'market_spot',
         'market_futures',
         'leverage',
         'amount',
         'running',
         'abort',
         'strategy',
         'created_at',
         )

    readonly_fields = ('name', 'amount', 'profit', 'running', 'abort')
    exclude = ['flgEnable', ]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class BotLoggerAdmin(admin.ModelAdmin):
    search_fields = ['bot__name']
    list_per_page = 20
    ordering = ('id',)
    list_display = (
        'created_at', 'user', 'profit', 'start_balance', 'end_balance', 'take_profit_ratio', 'stop_loss_ratio',
        'entry_candle',
        'entry_candle_date', 'take_profit',
        'candle_take_profit',
        'candle_take_profit_date', 'created_at',
        'stop_loss', 'candle_stop_loss', 'candle_stop_loss_date')
    exclude = ['flgEnable', ]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class StrategyBotAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = (
        'name', 'time_frame', 'description', 'logic_entry', 'logic_exit',)
    exclude = ['flgEnable', ]


class ExchangeAdmin(admin.ModelAdmin):
    search_fields = ['exchange']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('user', 'exchange', 'balance_futures', 'balance_spot',)
    readonly_fields = ('balance_futures', 'balance_spot')
    exclude = ['flgEnable', ]


class LogicExitAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name', 'takeprofit_long', 'takeprofit_short', 'stoploss_long', 'stoploss_short')
    exclude = ['flgEnable', ]


class LogicEntryAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name', 'ratio', 'sleep',)
    exclude = ['flgEnable', ]


admin.site.register(UserExchange, ExchangeAdmin)
admin.site.register(StrategyBot, StrategyBotAdmin)
admin.site.register(BotLogger, BotLoggerAdmin)
admin.site.register(Bot, BotAdmin)
admin.site.register(ClusterBot, ClusterBotAdmin)
admin.site.register(LogicEntry, LogicEntryAdmin)
admin.site.register(LogicExit, LogicExitAdmin)
admin.site.site_header = 'Amministrazione Crypto Engine'
