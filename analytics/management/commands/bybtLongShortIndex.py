from django.core.management import BaseCommand
from analytics.models import ByBt
import requests
import json
import logging
from analytics.model.indicator import btby_momentum
import csv
from datetime import datetime, timedelta

logger = logging.getLogger('main')


# 5 minutes =   https://fapi.bybt.com/api/futures/longShortChart?symbol=BTC&timeType=3
# 24H =         https://fapi.bybt.com/api/futures/longShortChart?symbol=BTC&timeType=5

class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):
        print(btby_momentum('KAVAUSDT'))
        # candle = 5
        # symbols = [
        #     'BTC',
        #     'ETH',
        #     'EOS',
        #     'LTC',
        #     'XRP',
        #     'BSV',
        #     'ETC',
        #     'TRX',
        #     'LINK',
        # ]
        #
        # try:
        #     for symbol in symbols:
        #         req = requests.get('https://fapi.bybt.com/api/futures/longShortChart?symbol=' + symbol + '&timeType=3')
        #         if req.status_code == 200:
        #             response = json.loads(req.content)
        #             logger.info(response)
        #             index = 0
        #             sum = 0
        #             longShortRateListLast = 0
        #
        #             symbol = symbol
        #             longRateList = response['data']['longRateList']
        #             shortsRateList = response['data']['shortsRateList']
        #             priceList = response['data']['priceList']
        #             longShortRateList = response['data']['longShortRateList']
        #
        #             dateList = response['data']['dateList']
        #             timeType = response['data']['timeType']
        #
        #             for k in longShortRateList:
        #                 sum += k
        #                 index += 1
        #                 longShortRateListLast = k
        #             avg = sum / index
        #
        #             ByBt.objects.create(
        #                 symbol=symbol,
        #                 longRateList=longRateList,
        #                 shortsRateList=shortsRateList,
        #                 priceList=priceList,
        #                 longShortRateList=longShortRateList,
        #                 longShortRateListLast=longShortRateListLast,
        #                 dateList=dateList,
        #                 timeType=timeType,
        #                 sum=sum,
        #                 avg=avg,
        #                 candle=candle,
        #                 time=5,
        #             )
        #
        # except Exception as e:
        #     logger.error(e)
        #     print("Exception: " + str(e))
