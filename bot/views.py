import json
from django.http import JsonResponse
from bot.services.telegram import Telegram
from django.views.decorators.csrf import csrf_exempt

telegram = Telegram()


@csrf_exempt
def webhook_tradingview(request):
    if request.method == 'POST':
        data = json.loads(request.data)
        telegram.send(data)

        return JsonResponse({})
