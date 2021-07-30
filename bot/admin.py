from django.contrib import admin
from bot.models import Bot, BotLogger


class BotAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'name', 'status', 'execution', 'live', 'strategy', 'quantity_investment',
        'leverage', 'binance_account', 'created_at', 'updated_at',)
    readonly_fields = ('name', 'execution',)
    exclude = ['flgEnable', ]


class BotLoggerAdmin(admin.ModelAdmin):
    search_fields = ['bot__name']
    list_per_page = 20
    ordering = ('id',)
    list_display = (
        'bot', 'created_at', 'entry_candle', 'entry_candle_date', 'take_profit', 'candle_take_profit',
        'candle_take_profit_date',
        'stop_loss', 'candle_stop_loss', 'candle_stop_loss_date', 'bot')
    exclude = ['flgEnable', ]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(BotLogger, BotLoggerAdmin)
admin.site.register(Bot, BotAdmin)

admin.site.site_header = 'Amministrazione TAS'
