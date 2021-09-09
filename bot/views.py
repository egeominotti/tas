import json
from django.http import JsonResponse
from bot.services.telegram import Telegram
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook_tradingview(request):
    if request.method == 'POST':
        telegram = Telegram()

        entry_text = "Test webook"
        telegram.send(entry_text)

        return JsonResponse({})
