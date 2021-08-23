import decouple
from django.core.management import BaseCommand
import logging
from strategy.models import SymbolExchange
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy
from bot.models import BufferRecordData
import redis
import unicorn_binance_websocket_api
import logging
import math
import os
import requests
import sys
import time
import threading
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
        # https://docs.python.org/3/library/logging.html#logging-levels
        logging.basicConfig(level=logging.ERROR,
                            filename=os.path.basename(__file__) + '.log',
                            format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                            style="{")

        symbolList = []
        for symbol in SymbolExchange.objects.all():
            symbolList.append(symbol.symbol.lower())

        # create instance of BinanceWebSocketApiManager
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com", output_default="UnicornFy")

        binance_websocket_api_manager.create_stream('kline_1m', symbolList, stream_label="kline_1m", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_5m', symbolList, stream_label="kline_5m", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_15m', symbolList, stream_label="kline_5m", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_30m', symbolList, stream_label="kline_30m", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_1h', symbolList, stream_label="kline_1h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_2h', symbolList, stream_label="kline_2h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_4h', symbolList, stream_label="kline_4h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_6h', symbolList, stream_label="kline_6h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_8h', symbolList, stream_label="kline_8h", output="UnicornFy")
        binance_websocket_api_manager.create_stream('kline_12h', symbolList, stream_label="kline_12h", output="UnicornFy")
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
                        if oldest_stream_data_from_stream_buffer['event_time'] >= oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
                            print(oldest_stream_data_from_stream_buffer['kline']['symbol'])
                            print(oldest_stream_data_from_stream_buffer['kline']['interval'])
                            print(oldest_stream_data_from_stream_buffer['kline']['open_price'])
                            print(oldest_stream_data_from_stream_buffer['kline']['close_price'])
                            print(oldest_stream_data_from_stream_buffer['kline']['high_price'])
                            print(oldest_stream_data_from_stream_buffer['kline']['low_price'])
                            print(oldest_stream_data_from_stream_buffer['kline']['is_closed'])
                            # print only the last kline
                            #print(f"UnicornFy: {oldest_stream_data_from_stream_buffer}")
                    except KeyError:
                        pass
                        #print(f"dict: {oldest_stream_data_from_stream_buffer}")
                    except TypeError:
                        pass
                        #print(f"raw_data: {oldest_stream_data_from_stream_buffer}")
        # r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)
        #
        # symbolList = []
        # for symbol in SymbolExchange.objects.all():
        #     symbolList.append(symbol.symbol.lower())
        #
        # # klines = ['kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_2h', 'kline_4h', 'kline_6h',
        # #           'kline_8h', 'kline_12h', 'kline_1d', 'kline_3d', 'kline_1w', 'kline_1M']
        #
        # klines = ['kline_1m',
        #           'kline_5m',
        #           'kline_15m',
        #           'kline_30m',
        #           'kline_1h',
        #           'kline_4h',
        #           'kline_1d',
        #           'kline_1w',
        #           'kline_1M']
        #
        # binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        # binance_websocket_api_manager.create_stream(klines, symbolList, output="UnicornFy")
        #
        # def save_data(v):
        #
        #     candle_is_closed = v.get('is_closed')
        #     symbol = v.get('symbol')
        #     interval = v.get('interval')
        #
        #     # Candle not closed - save to redis real time data
        #     key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval)
        #     candle_realtime = {
        #         'candle_close': float(v.get('close_price')),
        #         'candle_open': float(v.get('open_price')),
        #         'candle_high': float(v.get('high_price')),
        #         'candle_low': float(v.get('low_price')),
        #         'candle_is_closed': v.get('is_closed'),
        #         'time': v.get('kline_start_time')
        #     }
        #     print(candle_realtime)
        #     r.set(key, json.dumps(candle_realtime))
        #
        #     # candle_is_closed = v.get('is_closed')
        #     # symbol = v.get('symbol')
        #     # interval = v.get('interval')
        #     #
        #     # # Candle not closed - save to redis real time data
        #     # key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval)
        #     # candle_realtime = {
        #     #     'candle_close': float(v.get('close_price')),
        #     #     'candle_open': float(v.get('open_price')),
        #     #     'candle_high': float(v.get('high_price')),
        #     #     'candle_low': float(v.get('low_price')),
        #     #     'candle_is_closed': v.get('is_closed'),
        #     #     'time': v.get('kline_start_time')
        #     # }
        #     # r.set(key, json.dumps(candle_realtime))
        #
        #     # Candle closed - save to db
        #     # if candle_is_closed:
        #     #
        #     #     qs = BufferRecordData.objects.filter(key=key, is_closed=True).order_by('created_at')
        #     #
        #     #     if qs.count() >= 365:
        #     #         qs.first().delete()
        #     #
        #     #     if qs.count() <= 365:
        #     #         BufferRecordData.objects.create(
        #     #             key=key,
        #     #             symbol=symbol,
        #     #             time_frame=interval,
        #     #             open_candle=float(v.get('open_price')),
        #     #             close_candle=float(v.get('close_price')),
        #     #             high_candle=float(v.get('high_price')),
        #     #             low_candle=float(v.get('low_price')),
        #     #             is_closed=v.get('is_closed'),
        #     #             unix=v.get('kline_start_time'),
        #     #             volume=v.get('base_volume')
        #     #         )
        #
        # while True:
        #
        #     try:
        #
        #         oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        #         if oldest_stream_data_from_stream_buffer:
        #             binance_stream = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
        #             for k, v in binance_stream.items():
        #                 if isinstance(v, dict):
        #
        #                     worker_thread = threading.Thread(target=save_data, args=(v,),daemon=True)
        #                     worker_thread.start()
        #                     worker_thread.join()
        #
        #     except Exception as e:
        #         print(e)
        #         continue
