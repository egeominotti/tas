from django.contrib import admin
from exchange.models import Exchange, ExchangeList, User


class ExchangeAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_per_page = 50
    ordering = ('id',)
    readonly_fields = ('balance_futures', 'balance_spot')
    list_display = ('id', 'api_key', 'api_secret')
    exclude = ['flgEnable', ]


class ExchangeListAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


admin.site.register(User)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(ExchangeList, ExchangeListAdmin)
