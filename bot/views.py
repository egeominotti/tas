import datetime
from django.http import JsonResponse
from bot.services.telegram import Telegram
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def webhook_tradingview(request):
    telegram = Telegram()
    entry_text = "Test webook"
    telegram.send(entry_text)
    responseData = {
        'id': 4,
        'name': 'Test Response',
        'roles' : ['Admin','User']
    }

    return JsonResponse(responseData)
