from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import sys
from threading import Thread
import decouple
from binance import Client
from django.core.management import BaseCommand
from strategy.models import Coins
import redis
import logging
import time
import requests

logger = logging.getLogger('main')
import json

client = Client()
r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)

client.session.mount('https://', requests.adapters.HTTPAdapter(pool_maxsize=512))


def publish_kline(kline):

    symbol = kline['symbol']
    interval = kline['interval']
    kline_start_time = kline['kline_start_time']

    key = symbol + "_" + interval + "_FUTURES"

    klines = client \
        .futures_klines(symbol=symbol,
                        interval=interval,
                        endTime=kline_start_time,
                        limit=350)

    r.set(key, json.dumps(klines))
    r.publish(key, json.dumps({}))

    # if r.exists(key):
    #
    #     old_value = r.get(key)
    #     old_value = json.loads(old_value)
    #
    #     if len(old_value) == 100:
    #         del old_value[0]
    #
    #     old_value.append(candle_closed)
    #     print(len(old_value))
    #     r.set(key, json.dumps(old_value))
    #
    # else:
    #
    #     list = []
    #     list.append(candle_closed)
    #     r.set(key, json.dumps(list))

    # Close thread
    sys.exit()


class Command(BaseCommand):
    help = 'WebSocketStream Market Futures Binance'

    def handle(self, *args, **kwargs):

        symbolList = []
        for k in Coins.objects.all():
            symbolList.append(k.coins_exchange.symbol.lower())

        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures",
                                                                   output_default="UnicornFy")

        #binance_websocket_api_manager.create_stream('kline_1m', symbolList, stream_label="kline_1m", output="UnicornFy")
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

                        if oldest_stream_data_from_stream_buffer['event_time'] >= \
                                oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
                            if oldest_stream_data_from_stream_buffer['kline']['is_closed']:

                                thread = Thread(target=publish_kline,
                                                args=(oldest_stream_data_from_stream_buffer['kline'],))
                                thread.daemon = True
                                thread.start()

                    except KeyError:
                        pass
                    except TypeError:
                        pass
