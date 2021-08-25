import logging

import random
import requests
from django.core.management import BaseCommand
from bot.services.indicator import RealTimeIndicator

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'Valori real time delle candele'

    def handle(self, *args, **kwargs):
        dict = {}
        #
        # while True:
        #     indicator = RealTimeIndicator('RVNUSDT', '5m')
        #     indicator.compute(True)
        #     print(indicator.ema(5))
        #     print(indicator.rsi(14))
        #     print(indicator.bbands(20))
        #     print(indicator.candle())
        proxies_list = ['http://95.179.211.99:3129']

        proxies = {'http': random.choice(proxies_list)}

        req = requests.get(
            'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&google=true&speed=medium',
            proxies=proxies)
        val = req.json()['data']
        for k in val:
            ip = k.get('ip')
            port = k.get('port')
            protocols = k.get('protocols')[0]
            proxy = protocols + ip + port
            print(proxy)
            dict[protocols] = protocols + "//" + ip + ":" + port

        print(dict)
