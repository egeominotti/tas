from django.contrib import admin
from strategy.models import TimeFrame, SymbolExchange, SymbolTaapiApi, Coins


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
        'symbol',)
    exclude = ['flgEnable', ]


class SymbolTaapiApiAmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = (
        'symbol',)
    exclude = ['flgEnable', ]


class CoinsAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('coins_exchange',)
    exclude = ['flgEnable', ]


admin.site.register(TimeFrame, TimeFrameAdmin)
admin.site.register(SymbolExchange, SymbolExchangeAdmin)
admin.site.register(SymbolTaapiApi, SymbolTaapiApiAmin)
admin.site.register(Coins, CoinsAdmin)
