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
        logging.basicConfig(level=logging.DEBUG,
                            filename=os.path.basename(__file__) + '.log',
                            format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                            style="{")

        def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
            while True:
                if binance_websocket_api_manager.is_manager_stopping():
                    exit(0)
                oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
                if oldest_stream_data_from_stream_buffer is False:
                    time.sleep(0.01)

        # create instance of BinanceWebSocketApiManager for Binance.com Futures
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")

        # set api key and secret for userData stream
        binance_je_api_key = ""
        binance_je_api_secret = ""
        userdata_stream_id = binance_websocket_api_manager.create_stream(["arr"],
                                                                         ["!userData"],
                                                                         api_key=binance_je_api_key,
                                                                         api_secret=binance_je_api_secret)

        bookticker_all_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!bookTicker"])

        # https://binance-docs.github.io/apidocs/futures/en/#mark-price-stream-for-all-market
        binance_websocket_api_manager.create_stream(["!markPrice"], "arr@1s", stream_label="!markPrice@arr@1s")

        markets = {'btcusdt', 'bchusdt', 'ethusdt'}
        #binance_websocket_api_manager.create_stream(["aggTrade"], markets)
        #binance_websocket_api_manager.create_stream(["markPrice"], markets)
        binance_websocket_api_manager.create_stream(["kline_1m"], markets)
        binance_websocket_api_manager.create_stream(["kline_5m"], markets)
        binance_websocket_api_manager.create_stream(["kline_15m"], markets)
        binance_websocket_api_manager.create_stream(["kline_1h"], markets)
        binance_websocket_api_manager.create_stream(["kline_12h"], markets)
        # binance_websocket_api_manager.create_stream(["miniTicker"], markets)
        # binance_websocket_api_manager.create_stream(["bookTicker"], markets)
        # binance_websocket_api_manager.create_stream(["depth"], markets)
        # binance_websocket_api_manager.create_stream(["depth@2500ms"], markets)
        # binance_websocket_api_manager.create_stream(["depth5"], markets)
        # binance_websocket_api_manager.create_stream(["depth5@100ms"], markets)
        # binance_websocket_api_manager.create_stream(["depth10"], markets)
        # binance_websocket_api_manager.create_stream(["depth20"], markets)
        binance_websocket_api_manager.create_stream(["compositeIndex"], markets, stream_label="compositeIndex")

        channels = {'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_12h'}
        binance_websocket_api_manager.create_stream(channels, markets)

        # start a worker process to move the received stream_data from the stream_buffer to a print function
        worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer,
                                         args=(binance_websocket_api_manager,))
        worker_thread.start()

        # show an overview
        while True:
            binance_websocket_api_manager.print_summary()
            time.sleep(1)
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
