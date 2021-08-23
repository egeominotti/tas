import datetime

import decouple
from django.core.management import BaseCommand
import logging
from strategy.models import SymbolExchange
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy
from bot.models import BufferRecordData
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

        # times = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
        #
        # for symbol in symbolList:
        #     for interval in times:
        #         key = str(SymbolExchange.objects.get(symbol=symbol.upper())) + "_" + str(interval)
        #         data[key] = {'data': [] }
        #
        # print(data)

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
                        # if candle is closed save record
                        if oldest_stream_data_from_stream_buffer['event_time'] >= \
                                oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
                            if oldest_stream_data_from_stream_buffer['kline']['is_closed']:

                                try:

                                    kline =                     oldest_stream_data_from_stream_buffer['kline']
                                    symbol =                    kline['symbol']
                                    interval =                  kline['interval']
                                    open_price =                kline['open_price']
                                    close_price =               kline['close_price']
                                    high_price =                kline['high_price']
                                    low_price =                 kline['low_price']
                                    is_closed =                 kline['is_closed']
                                    kline_start_time =          kline['kline_start_time']

                                    key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval) + "_CLOSED"

                                    candle_realtime = {

                                        'candle_close': close_price,
                                        'candle_open': open_price,
                                        'candle_high': high_price,
                                        'candle_low': low_price,
                                        'is_closed': is_closed,
                                        'time_milliseconds': kline_start_time,
                                        #'time_datetime': datetime.datetime.fromtimestamp(kline['kline_start_time'] / 1000.0,tz=datetime.timezone.utc),
                                    }

                                    if r.exists(key):
                                        old_value = r.get(key)
                                        old_value = json.loads(old_value)

                                        print("CLOSED")
                                        print(len(old_value))

                                        if len(old_value) >= 500:
                                            del old_value[0]

                                        old_value.append(candle_realtime)
                                        r.set(key, json.dumps(old_value))

                                    else:
                                        list = []
                                        list.append(candle_realtime)
                                        r.set(key, json.dumps(list))

                                except Exception as e:
                                    print(str(e))
                        else:
                            try:

                                kline = oldest_stream_data_from_stream_buffer['kline']
                                symbol = kline['symbol']
                                interval = kline['interval']
                                open_price = kline['open_price']
                                close_price = kline['close_price']
                                high_price = kline['high_price']
                                low_price = kline['low_price']
                                is_closed = kline['is_closed']
                                kline_start_time = kline['kline_start_time']

                                key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval) + "_REALTIME"

                                candle_realtime = {

                                    'candle_close': close_price,
                                    'candle_open': open_price,
                                    'candle_high': high_price,
                                    'candle_low': low_price,
                                    'is_closed': is_closed,
                                    'time_milliseconds': kline_start_time,
                                    # 'time_datetime': datetime.datetime.fromtimestamp(kline['kline_start_time'] / 1000.0,tz=datetime.timezone.utc),
                                }

                                if r.exists(key):
                                    old_value = r.get(key)
                                    old_value = json.loads(old_value)

                                    print("REALTIME")
                                    print(len(old_value))

                                    if len(old_value) >= 500:
                                        del old_value[0]

                                    old_value.append(candle_realtime)
                                    r.set(key, json.dumps(old_value))

                                else:
                                    list = []
                                    list.append(candle_realtime)
                                    r.set(key, json.dumps(list))

                            except Exception as e:
                                print(str(e))

                    except KeyError as e:
                        pass
                        # print(str(e))
                    except TypeError as e:
                        pass
                        # print(str(e))
                    except Exception as e:
                        print(str(e))

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
