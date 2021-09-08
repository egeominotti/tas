from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import sys
from threading import Thread
import decouple
from binance import Client
from django.core.management import BaseCommand
from strategy.models import SymbolExchange
import redis
import logging
import time
import requests

logger = logging.getLogger('main')
import json

r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)
r.flushall()

LIMIT_KLINE = 348
KEY = 'SPOT'


def save_klines(kline):
    symbol = kline['symbol']
    interval = kline['interval']
    kline_start_time = kline['kline_start_time']

    key = symbol + "_" + interval + "_" + KEY

    # Solo la prima volta scarico i dati la seconda volta li accodo
    if r.exists(key):

        old_value = r.get(key)
        pre_kline = json.loads(old_value)

        if len(pre_kline) == 350:
            pre_kline.pop(0)

        kline_from_websocket = [kline['kline_start_time'],
                                kline['open_price'],
                                kline['high_price'],
                                kline['low_price'],
                                kline['close_price'], ]

        pre_kline.append(kline_from_websocket)
        r.set(key, json.dumps(pre_kline))

    # La prima volta scarico i dati dato che non esiste la chiave
    else:

        client = Client()

        klines = client \
            .get_klines(symbol=symbol,
                        interval=interval,
                        endTime=kline_start_time,
                        limit=LIMIT_KLINE)

        r.set(key, json.dumps(klines))

    # Close thread
    sys.exit()


def send_realtime_candle_close(kline):

    symbol = kline['symbol']
    interval = kline['interval']
    key = symbol + "_" + interval + "_" + KEY + "_CANDLE"

    close_price = kline['close_price']
    open_price = kline['open_price']
    high_price = kline['high_price']
    low_price = kline['low_price']

    candle = {'close': float(close_price),
              'open': float(open_price),
              'low': float(low_price),
              'high': float(high_price)}

    r.set(key, json.dumps(candle))

    # Close thread
    sys.exit()


class Command(BaseCommand):
    help = 'WebSocketStream Market Spot Binance'

    def handle(self, *args, **kwargs):
        pass
        # counter = 0
        # symbolList = []
        # for k in SymbolExchange.objects.filter(exchange='binance'):
        #     symbolList.append(k.symbol.lower())
        #
        # binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com",
        #                                                            output_default="UnicornFy")
        #
        # binance_websocket_api_manager.create_stream('kline_5m', symbolList, output="UnicornFy")
        #
        # while True:
        #
        #     if binance_websocket_api_manager.is_manager_stopping():
        #         r.flushall()
        #         exit(0)
        #     oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        #
        #     if oldest_stream_data_from_stream_buffer is False:
        #         time.sleep(0.01)
        #     else:
        #
        #         if oldest_stream_data_from_stream_buffer is not None:
        #             try:
        #                 if not oldest_stream_data_from_stream_buffer['kline']['is_closed']:
        #                     thread = Thread(target=send_realtime_candle_close,
        #                                     args=(oldest_stream_data_from_stream_buffer['kline'],))
        #                     thread.daemon = True
        #                     thread.start()
        #
        #                 if oldest_stream_data_from_stream_buffer['event_time'] >= \
        #                         oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
        #                     if oldest_stream_data_from_stream_buffer['kline']['is_closed']:
        #
        #                         thread = Thread(target=save_klines,
        #                                         args=(oldest_stream_data_from_stream_buffer['kline'],))
        #                         thread.daemon = True
        #                         thread.start()
        #
        #                         counter += 1
        #
        #                         if len(symbolList) == counter:
        #                             r.publish(oldest_stream_data_from_stream_buffer['kline']['interval'],
        #                                       json.dumps({'status': True}))
        #                             counter = 0
        #
        #             except KeyError:
        #                 pass
        #             except TypeError:
        #                 pass
