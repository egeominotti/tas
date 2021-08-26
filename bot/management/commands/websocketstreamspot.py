import datetime
from threading import Thread
import decouple
from binance import Client
from django.core.management import BaseCommand
import logging
from strategy.models import SymbolExchange
import redis
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import logging
import os
import time

logger = logging.getLogger('main')
import json

LIMIT_KLINE = 300
client = Client()
r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)

def update_keys(kline):

    symbol = kline['symbol']
    interval = kline['interval']
    kline_start_time = kline['kline_start_time']
    key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval) + "_SPOT"

    klines = client \
        .get_klines(symbol=symbol,
                        interval=interval,
                        endTime=kline_start_time,
                        limit=LIMIT_KLINE)

    r.set(key, json.dumps(klines))

class Command(BaseCommand):
    help = 'WebSocketStream Market Spot Binance'

    def handle(self, *args, **kwargs):

        symbolList = []
        for symbol in SymbolExchange.objects.all():
            symbolList.append(symbol.symbol.lower())

        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com", output_default="UnicornFy")

        binance_websocket_api_manager.create_stream('kline_1m', symbolList, stream_label="kline_1m", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_5m', symbolList, stream_label="kline_5m", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_15m', symbolList, stream_label="kline_5m",
                                                    output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_30m', symbolList, stream_label="kline_30m",
                                                    output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_1h', symbolList, stream_label="kline_1h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_2h', symbolList, stream_label="kline_2h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_4h', symbolList, stream_label="kline_4h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_6h', symbolList, stream_label="kline_6h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_8h', symbolList, stream_label="kline_8h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_12h', symbolList, stream_label="kline_12h",
                                                    output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_1d', symbolList, stream_label="kline_1d", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_3d', symbolList, stream_label="kline_3d", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_1w', symbolList, stream_label="kline_1w", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_1M', symbolList, stream_label="kline_1M", output="UnicornFy")

        while True:

            if binance_websocket_api_manager.is_manager_stopping():
                exit(0)
            oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()

            if oldest_stream_data_from_stream_buffer is False:
                time.sleep(0.01)
            else:

                if oldest_stream_data_from_stream_buffer is not None:
                    try:
                        if not oldest_stream_data_from_stream_buffer['kline']['is_closed']:
                            pass


                        if oldest_stream_data_from_stream_buffer['event_time'] >= \
                                oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
                            # print only the last kline
                            if oldest_stream_data_from_stream_buffer['kline']['is_closed']:

                                kline = oldest_stream_data_from_stream_buffer['kline']
                                thread = Thread(target=update_keys, args=(kline,))
                                thread.daemon = True
                                thread.start()
                                thread.join()

                    except KeyError:
                        pass
                    except TypeError:
                        pass
