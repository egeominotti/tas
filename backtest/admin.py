from django.contrib import admin
from backtest.models import BackTest, BackTestLog, StrategyBacktesting, StatisticsPortfolio, LogicExit, LogicEntry
from csvexport.actions import csvexport


class BackTestLogAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    actions = [csvexport]
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'backtest', 'time_frame', 'symbol', 'entry_candle_date', 'entry_candle',
        'candle_stop_loss_date', 'candle_stop_loss', 'stop_loss', 'loss_percentage',
        'candle_take_profit_date', 'candle_take_profit', 'take_profit', 'profit_percentage')
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
    list_display = (
        'backtest', 'initial_investment', 'current_wallet', 'composite_value', 'entry', 'take_profit', 'stop_loss')
    exclude = ['flgEnable', ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class BackTestAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('strategy', 'start_period', 'start_period', 'running', 'scheduled', 'error')
    readonly_fields = ('scheduled', 'error')
    exclude = ['flgEnable', ]


class StrategyBacktestingAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name', 'time_frame', 'logic_entry', 'logic_exit', 'symbol_exchange')
    exclude = ['flgEnable', ]


class LogicEntryAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name', 'ratio',)
    exclude = ['flgEnable', ]


class LogicExitAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('name', 'takeprofit', 'stoploss',)
    exclude = ['flgEnable', ]


admin.site.register(LogicEntry, LogicEntryAdmin)
admin.site.register(LogicExit, LogicExitAdmin)
admin.site.register(StrategyBacktesting, StrategyBacktestingAdmin)
admin.site.register(BackTestLog, BackTestLogAdmin)
admin.site.register(BackTest, BackTestAdmin)
admin.site.register(StatisticsPortfolio, StatisticsPortfolioAdmin)
