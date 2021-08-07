from django.contrib import admin
from bot.models import Bot, BotLogger, StrategyBot
from bot.models import UserExchange


class BotAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'name', 'user', 'running', 'abort', 'strategy', 'coins', 'created_at', 'updated_at',)
    readonly_fields = ('name', 'abort')
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
        'user', 'entry_candle', 'entry_candle_date', 'take_profit', 'candle_take_profit',
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
    list_display = ('user', 'exchange', 'balance_futures', 'balance_spot', 'leverage', 'live')
    readonly_fields = ('balance_futures', 'balance_spot')
    exclude = ['flgEnable', ]


admin.site.register(UserExchange, ExchangeAdmin)
admin.site.register(StrategyBot, StrategyBotAdmin)
admin.site.register(BotLogger, BotLoggerAdmin)
admin.site.register(Bot, BotAdmin)

admin.site.site_header = 'Amministrazione TAS'
