from django.contrib import admin
from exchange.models import ExchangeList, User




class ExchangeListAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    list_display = ('id', 'name')
    exclude = ['flgEnable', ]


class UtenteAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 50
    ordering = ('id',)
    readonly_fields = ('counter_bot',)
    list_display = ('username',)
    exclude = ['flgEnable', ]


admin.site.register(User, UtenteAdmin)
admin.site.register(ExchangeList, ExchangeListAdmin)
