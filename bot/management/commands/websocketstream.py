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
logger = logging.getLogger('main')
import json


class Command(BaseCommand):
    help = 'WebSocketStream Binance'

    def handle(self, *args, **kwargs):


        try:
            import unicorn_binance_rest_api
        except ImportError:
            print("Please install `unicorn-binance-rest-api`! https://pypi.org/project/unicorn-binance-rest-api/")
            sys.exit(1)

        binance_api_key = ""
        binance_api_secret = ""
        channels = {'aggTrade', 'trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_2h',
                    'kline_4h',
                    'kline_6h', 'kline_8h', 'kline_12h', 'kline_1d', 'kline_3d', 'kline_1w', 'kline_1M', 'miniTicker',
                    'ticker', 'bookTicker', 'depth5', 'depth10', 'depth20', 'depth', 'depth@100ms'}
        arr_channels = {'!miniTicker', '!ticker', '!bookTicker'}

        # https://docs.python.org/3/library/logging.html#logging-levels
        logging.basicConfig(level=logging.INFO,
                            filename=os.path.basename(__file__) + '.log',
                            format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                            style="{")

        def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
            while True:
                if binance_websocket_api_manager.is_manager_stopping():
                    exit(0)
                oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
                if oldest_stream_data_from_stream_buffer is not False:
                    pass
                else:
                    time.sleep(0.01)

        try:
            binance_rest_client = unicorn_binance_rest_api.BinanceRestApiManager(binance_api_key, binance_api_secret)
        except requests.exceptions.ConnectionError:
            print("No internet connection?")
            sys.exit(1)

        binance_websocket_api_manager = unicorn_binance_websocket_api.BinanceWebSocketApiManager()

        # start a worker process to move the received stream_data from the stream_buffer to a print function
        worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer,
                                         args=(binance_websocket_api_manager,))
        worker_thread.start()

        markets = []
        data = binance_rest_client.get_all_tickers()
        for item in data:
            markets.append(item['symbol'])

        private_stream_id_alice = binance_websocket_api_manager.create_stream(["!userData"],
                                                                              ["arr"],
                                                                              api_key=binance_api_key,
                                                                              api_secret=binance_api_secret,
                                                                              stream_label="userData Alice")

        private_stream_id_bob = binance_websocket_api_manager.create_stream(["!userData"],
                                                                            ["arr"],
                                                                            api_key="aaa",
                                                                            api_secret="bbb",
                                                                            stream_label="userData Bob")

        arr_stream_id = binance_websocket_api_manager.create_stream(arr_channels, "arr", stream_label="arr channels",
                                                                    ping_interval=10, ping_timeout=10, close_timeout=5)

        divisor = math.ceil(len(markets) / binance_websocket_api_manager.get_limit_of_subscriptions_per_stream())
        max_subscriptions = math.ceil(len(markets) / divisor)

        for channel in channels:
            if len(markets) <= max_subscriptions:
                binance_websocket_api_manager.create_stream(channel, markets, stream_label=channel)
            else:
                loops = 1
                i = 1
                markets_sub = []
                for market in markets:
                    markets_sub.append(market)
                    if i == max_subscriptions or loops * max_subscriptions + i == len(markets):
                        binance_websocket_api_manager.create_stream(channel, markets_sub,
                                                                    stream_label=str(channel + "_" + str(i)),
                                                                    ping_interval=10, ping_timeout=10, close_timeout=5)
                        markets_sub = []
                        i = 1
                        loops += 1
                    i += 1

        while True:
            binance_websocket_api_manager.print_summary()
            # binance_websocket_api_manager.print_stream_info(arr_stream_id)
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
        #                     candle_is_closed = v.get('is_closed')
        #                     symbol = v.get('symbol')
        #                     interval = v.get('interval')
        #
        #                     # Candle not closed - save to redis real time data
        #                     key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval)
        #                     candle_realtime = {
        #                         'candle_close': float(v.get('close_price')),
        #                         'candle_open': float(v.get('open_price')),
        #                         'candle_high': float(v.get('high_price')),
        #                         'candle_low': float(v.get('low_price')),
        #                         'candle_is_closed': v.get('is_closed'),
        #                         'time': v.get('kline_start_time')
        #                     }
        #                     r.set(key, json.dumps(candle_realtime))
        #
        #                     # Candle closed - save to db
        #                     # if candle_is_closed:
        #                     #
        #                     #     qs = BufferRecordData.objects.filter(key=key, is_closed=True).order_by('created_at')
        #                     #
        #                     #     if qs.count() >= 365:
        #                     #         qs.first().delete()
        #                     #
        #                     #     if qs.count() <= 365:
        #                     #         BufferRecordData.objects.create(
        #                     #             key=key,
        #                     #             symbol=symbol,
        #                     #             time_frame=interval,
        #                     #             open_candle=float(v.get('open_price')),
        #                     #             close_candle=float(v.get('close_price')),
        #                     #             high_candle=float(v.get('high_price')),
        #                     #             low_candle=float(v.get('low_price')),
        #                     #             is_closed=v.get('is_closed'),
        #                     #             unix=v.get('kline_start_time'),
        #                     #             volume=v.get('base_volume')
        #                     #         )
        #
        #     except Exception as e:
        #         print(e)
        #         continue
