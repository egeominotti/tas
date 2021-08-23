import datetime

import decouple
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


class Command(BaseCommand):
    help = 'WebSocketStream Binance'

    def handle(self, *args, **kwargs):

        r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)

        logging.basicConfig(level=logging.ERROR,
                            filename=os.path.basename(__file__) + '.log',
                            format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                            style="{")

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
                            #print("NON CHIUSE")
                            # print(f"UnicornFy: {oldest_stream_data_from_stream_buffer}")

                        if oldest_stream_data_from_stream_buffer['event_time'] >= \
                                oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
                            # print only the last kline
                            if oldest_stream_data_from_stream_buffer['kline']['is_closed']:

                                kline = oldest_stream_data_from_stream_buffer['kline']
                                symbol = kline['symbol']
                                interval = kline['interval']
                                open_price = kline['open_price']
                                close_price = kline['close_price']
                                high_price = kline['high_price']
                                low_price = kline['low_price']
                                is_closed = kline['is_closed']
                                kline_start_time = kline['kline_start_time']

                                key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval)

                                candle_closed = {
                                    'candle_close': close_price,
                                    'candle_open': open_price,
                                    'candle_high': high_price,
                                    'candle_low': low_price,
                                    'is_closed': is_closed,
                                    'time_milliseconds': kline_start_time,
                                }

                                if r.exists(key):

                                    old_value = r.get(key)
                                    old_value = json.loads(old_value)

                                    print(len(old_value))

                                    if len(old_value) == 15:
                                        del old_value[0]

                                    old_value.append(candle_closed)
                                    r.set(key, json.dumps(old_value))

                                else:

                                    list = []
                                    list.append(candle_closed)
                                    r.set(key, json.dumps(list))

                    except KeyError:
                        pass
                        # print(f"dict: {oldest_stream_data_from_stream_buffer}")
                    except TypeError:
                        pass
                        # print(f"raw_data: {oldest_stream_data_from_stream_buffer}")
