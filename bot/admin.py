from django.contrib import admin
from bot.models import Bot


class BotAdmin(admin.ModelAdmin):
    search_fields = ['tf']
    list_per_page = 50
    ordering = ('id',)


admin.site.register(Bot, BotAdmin)
