from django.contrib import admin
from exchange.models import Exchange, ExchangeList


class ExchangeAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'user', 'api_key', 'api_secret')
    exclude = ['flgEnable', ]


class ExchangeListAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(ExchangeList, ExchangeListAdmin)
