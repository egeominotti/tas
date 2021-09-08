from time import sleep
import datetime
import decouple
import json
import redis
from django.core.management import BaseCommand
import logging
from backtest.services.computedata import compute_data_to_store
from bot.models import ComputedData
from bot.services.telegram import Telegram
from strategy.models import SymbolExchange, TimeFrame

logger = logging.getLogger('main')

r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)


class Command(BaseCommand):
    help = 'Indicator Calculator'

    def handle(self, *args, **kwargs):

        telegram = Telegram()
        symbols = SymbolExchange.objects.filter(market='FUTURES')
        time_frame = TimeFrame.objects.all()

        ComputedData.objects.all().delete()
        for interval in time_frame:
            for coin in symbols:
                key = str(coin.symbol) + "_" + str(interval) + "_" + coin.market
                if r.exists(key):
                    klines = json.loads(r.get(key))
                    if len(klines) > 0:

                        computed_data = compute_data_to_store(klines)
                        val = json.loads(computed_data)

                        if val.get('rsi') is not None:

                            rsi = round(val.get('rsi'), coin.quantity_precision)
                            close = round(val.get('close'), coin.quantity_precision)
                            ema200 = round(val.get('ema200'), coin.quantity_precision)
                            ema50 = round(val.get('ema50'), coin.quantity_precision)
                            ema5 = round(val.get('ema5'), coin.quantity_precision)
                            ema10 = round(val.get('ema10'), coin.quantity_precision)
                            upperband = round(val.get('upperband'), coin.quantity_precision)
                            middleband = round(val.get('middleband'), coin.quantity_precision)
                            lowerband = round(val.get('lowerband'), coin.quantity_precision)

                            # Long signal
                            if ema200 < close:
                                if rsi < 30 and close <= lowerband:
                                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                                    message = '‼️+ Entry Long: ' + coin.symbol + " " \
                                              "\n" + 'Candle close: ' + str(close) + \
                                              "\n" + 'Time Frame: ' + str(interval) + \
                                              "\n" + "Candle Close: " + str(close) + \
                                              "\n" + "RSI: " + str(rsi) + \
                                              "\n" + "Upperband: " + str(upperband) + \
                                              "\n" + "Middleband: " + str(middleband) + \
                                              "\n" + "Lowerband: " + str(lowerband) + \
                                              "\n" + "ema200: " + str(ema200) + \
                                              "\n" + "Date: " + str(now)
                                    telegram.send(message)

                            # Short signal
                            if ema200 > close:
                                if rsi > 70 and close >= upperband:
                                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                                    message = '‼️+ Entry Short: ' + coin.symbol + " " \
                                              "\n" + 'Candle close: ' + str(close) + \
                                              "\n" + 'Time Frame: ' + str(interval) + \
                                              "\n" + "Candle Close: " + str(close) + \
                                              "\n" + "RSI: " + str(rsi) + \
                                              "\n" + "Upperband: " + str(upperband) + \
                                              "\n" + "Middleband: " + str(middleband) + \
                                              "\n" + "Lowerband: " + str(lowerband) + \
                                              "\n" + "ema200: " + str(ema200) + \
                                              "\n" + "Date: " + str(now)
                                    telegram.send(message)

                            # Short signal
                            # if rsi >= 80 and close >= upperband:
                            #     now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            #     message = '‼️+  Entry Short: ' + coin.symbol + " " \
                            #               "\n" + 'Time Frame: ' + str(interval) + \
                            #               "\n" + "Candle Close: " + str(close) + \
                            #               "\n" + "RSI: " + str(rsi) + \
                            #               "\n" + "Upperband: " + str(upperband) + \
                            #               "\n" + "Middleband: " + str(middleband) + \
                            #               "\n" + "Lowerband: " + str(lowerband) + \
                            #               "\n" + "Date: " + str(now)
                            #
                            #     telegram.send(message)

                        ComputedData.objects.create(
                            key=key,
                            symbol=coin.symbol,
                            time_frame=interval,
                            data=computed_data
                        )
