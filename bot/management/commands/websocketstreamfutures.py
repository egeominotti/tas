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
# client.session.mount('https://', requests.adapters.HTTPAdapter(pool_maxsize=256))

LIMIT_KLINE = 348


def save_klines(kline):
    symbol = kline['symbol']
    interval = kline['interval']
    kline_start_time = kline['kline_start_time']

    key = symbol + "_" + interval + "_FUTURES"

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

        # Publish message to bot
        # r.publish(key, json.dumps({}))

    # La prima volta scarico i dati dato che non esiste la chiave
    else:

        client = Client()

        klines = client \
            .futures_klines(symbol=symbol,
                            interval=interval,
                            endTime=kline_start_time,
                            limit=LIMIT_KLINE)

        r.set(key, json.dumps(klines))

        # Publish message to bot
        # r.publish(key, json.dumps({}))

    # Close thread
    sys.exit()


def send_realtime_candle_close(kline):

    symbol = kline['symbol']
    interval = kline['interval']
    key = symbol + "_" + interval + "_FUTURES_CANDLE"
    close_price = kline['close_price']
    candle = {'close': float(close_price)}
    r.set(key, json.dumps(candle))

    # Close thread
    sys.exit()


class Command(BaseCommand):
    help = 'WebSocketStream Market Futures Binance'

    def handle(self, *args, **kwargs):

        symbolList = []
        for k in SymbolExchange.objects.all():
            symbolList.append(k.symbol.lower())

        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures",
                                                                   output_default="UnicornFy")

        binance_websocket_api_manager.create_stream('kline_5m', symbolList, output="UnicornFy")
        # binance_websocket_api_manager.create_stream('kline_4h', symbolList, output="UnicornFy")
        # binance_websocket_api_manager.create_stream('kline_1d', symbolList, output="UnicornFy")

        while True:

            if binance_websocket_api_manager.is_manager_stopping():
                r.flushall()
                exit(0)
            oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()

            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)
            else:

                if oldest_stream_data_from_stream_buffer is not None:
                    try:
                        if not oldest_stream_data_from_stream_buffer['kline']['is_closed']:
                            thread = Thread(target=send_realtime_candle_close,
                                            args=(oldest_stream_data_from_stream_buffer['kline'],))
                            thread.daemon = True
                            thread.start()

                        if oldest_stream_data_from_stream_buffer['event_time'] >= \
                                oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
                            if oldest_stream_data_from_stream_buffer['kline']['is_closed']:
                                interval = oldest_stream_data_from_stream_buffer['kline']['interval']
                                r.set(interval, json.dumps({'closed': True}))

                                thread = Thread(target=save_klines,
                                                args=(oldest_stream_data_from_stream_buffer['kline'],))
                                thread.daemon = True
                                thread.start()

                    except KeyError:
                        pass
                    except TypeError:
                        pass
