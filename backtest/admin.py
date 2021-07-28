from django.contrib import admin

from django.contrib import admin
from backtest.models import BackTest, StatisticsPortfolio


class BackTestAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'id', 'algorithm', 'time_frame', 'symbol', 'entry_candle', 'stop_loss', 'take_profit', 'candle_stop_loss',
        'candle_take_profit')
    exclude = ['flgEnable', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class StatisticsPortfolioAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'algorithm', 'entry', 'time_frame', 'take_profit', 'stop_loss', 'profit_ratio', 'loss_ratio',
                    'profit_loss_percentage', 'function_name_take_profit', 'function_name_stop_loss')
    exclude = ['flgEnable', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(BackTest, BackTestAdmin)
admin.site.register(StatisticsPortfolio, StatisticsPortfolioAdmin)
