import csv
from django.contrib import admin
from django.http import HttpResponse
from backtest.models import *
from csvexport.actions import csvexport


class BackTestLogAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    actions = [csvexport]
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'time_frame', 'symbol', 'entry_candle_date', 'entry_candle',
        'candle_stop_loss_date', 'candle_stop_loss', 'stop_loss',
        'candle_take_profit_date', 'candle_take_profit', 'take_profit',)
    exclude = ['flgEnable', ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class StatisticsPortfolioAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    actions = [csvexport]
    list_display = ('entry', 'time_frame', 'take_profit', 'stop_loss', 'profit_ratio', 'loss_ratio',
                    'profit_loss_percentage',)
    exclude = ['flgEnable', ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class BackTestAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('strategy', 'start_period', 'start_period', 'scheduled', 'error')
    readonly_fields = ('scheduled', 'error')
    exclude = ['flgEnable', ]


admin.site.register(BackTestLog, BackTestLogAdmin)
admin.site.register(BackTest, BackTestAdmin)
admin.site.register(StatisticsPortfolio, StatisticsPortfolioAdmin)
