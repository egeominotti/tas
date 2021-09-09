import datetime
import json

from django.http import JsonResponse
from bot.services.telegram import Telegram
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook_tradingview(request):
    telegram = Telegram()
    entry_text = "Test webook"
    data = json.loads(request.body)
    telegram.send(entry_text)

    return JsonResponse({'test': 1})
