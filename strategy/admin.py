from django.contrib import admin
from strategy.models import TimeFrame, SymbolExchange, SymbolTaapiApi


class TimeFrameAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('id',)
    list_display = ('time_frame',)
    exclude = ['flgEnable', ]


class SymbolExchangeAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'id', 'exchange', 'market', 'symbol', 'precision', 'quantity_precision')
    exclude = ['flgEnable', ]


# class SymbolTaapiApiAmin(admin.ModelAdmin):
#     search_fields = ['tf']
#     list_per_page = 50
#     ordering = ('id',)
#     list_display = (
#         'symbol',)
#     exclude = ['flgEnable', ]


admin.site.register(TimeFrame, TimeFrameAdmin)
admin.site.register(SymbolExchange, SymbolExchangeAdmin)
#admin.site.register(SymbolTaapiApi, SymbolTaapiApiAmin)
