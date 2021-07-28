import csv

from django.contrib import admin

from django.contrib import admin
from django.http import HttpResponse

from backtest.models import BackTest, StatisticsPortfolio


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


admin.site.register(BackTest, BackTestAdmin)
admin.site.register(StatisticsPortfolio, StatisticsPortfolioAdmin)
