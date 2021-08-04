import json

import requests


def btby_momentum(symbol):
    req = requests.get('https://fapi.bybt.com/api/futures/longShortChart?symbol=' + symbol + '&timeType=3')
    if req.status_code == 200:
        response = json.loads(req.content)
        longShortRateList = response['data']['longShortRateList']
        longShortRate = longShortRateList[-1]
        if longShortRate is not None and longShortRate > 0:
            return longShortRate
        else:
            return None
