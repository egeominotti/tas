import threading

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

logger = logging.getLogger('main')
import json


class Command(BaseCommand):
    help = 'WebSocketStream Market Futures Binance'

    def handle(self, *args, **kwargs):

        def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
            while True:
                if binance_websocket_api_manager.is_manager_stopping():
                    exit(0)
                oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
                if oldest_stream_data_from_stream_buffer is False:
                    time.sleep(0.01)
                else:
                    print(oldest_stream_data_from_stream_buffer)

        # configure api key and secret for binance.com
        api_key = ""
        api_secret = ""

        # create instances of BinanceWebSocketApiManager
        ubwa_com = BinanceWebSocketApiManager(exchange="binance.com-futures")
        user_stream_id = ubwa_com.create_stream('arr', '!userData', api_key='vyghMLzH2Pvr0TCoV11Equ9kIK2jxL6ZpDh8pyUBz4hvAWXSLWO6rBHbogQmX9lH', api_secret='yTmr8uu0w3ARIzTlYadGkWX79BlTHSybzzJeInrWcjUoygP3K7t81j4WXd8amMOM')

        # start a worker process to move the received stream_data from the stream_buffer to a print function
        worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(ubwa_com,))
        worker_thread.start()


        # monitor the streams
        while True:
            ubwa_com.print_stream_info(user_stream_id)
            time.sleep(1)
