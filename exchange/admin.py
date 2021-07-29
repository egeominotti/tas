from django.contrib import admin
from exchange.models import BinanceAccount


class BinanceAccountAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'user', 'api_key', 'api_secret')
    exclude = ['flgEnable', ]


admin.site.register(BinanceAccount, BinanceAccountAdmin)
