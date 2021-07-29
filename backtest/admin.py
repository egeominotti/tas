import csv
from django.contrib import admin
from django.http import HttpResponse
from backtest.models import *


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Esporta elementi selezionati"


class BackTestAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'id', 'algorithm', 'time_frame', 'symbol', 'entry_candle', 'stop_loss', 'take_profit', 'candle_stop_loss',
        'candle_take_profit')
    actions = ["export_as_csv"]
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
    actions = ["export_as_csv"]

    list_display = ('id', 'algorithm', 'entry', 'time_frame', 'take_profit', 'stop_loss', 'profit_ratio', 'loss_ratio',
                    'profit_loss_percentage', 'function_name_take_profit', 'function_name_stop_loss')
    exclude = ['flgEnable', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


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
    list_display = ('id', 'name', 'logic_entry', 'logic_takeprofit', 'logic_stoploss',)
    exclude = ['flgEnable', ]


class TimeFrameAdmin(admin.ModelAdmin):
    # search_fields = ['time_frame']
    list_per_page = 20
    ordering = ('id',)
    list_display = ('time_frame', 'to_import')
    exclude = ['flgEnable', ]


class LogicEntryAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


class LogicTakepProfitAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


class LogicStopLossAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


admin.site.register(TimeFrame, TimeFrameAdmin)
admin.site.register(SymbolExchange, SymbolExchangeAdmin)
admin.site.register(SymbolTaapiApi, SymbolTaapiApiAmin)
admin.site.register(Strategy, StrategyDispatcherAdmin)
admin.site.register(LogicEntry, LogicEntryAdmin)
admin.site.register(LogicTakepProfit, LogicTakepProfitAdmin)
admin.site.register(LogicStopLoss, LogicStopLossAdmin)
admin.site.register(BackTest, BackTestAdmin)
admin.site.register(StatisticsPortfolio, StatisticsPortfolioAdmin)
