import json

import datetime
from time import sleep

from decouple import config
from django.core.management import BaseCommand
import logging
from strategy.models import LogicEntry
from html_sanitizer import Sanitizer
from backtest.services.util import find_prev_candle
from binance import ThreadedWebsocketManager
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import UnicornFy
logger = logging.getLogger('main')

#twm = ThreadedWebsocketManager(api_key=config('API_KEY_BINANCE'), api_secret=config('API_SECRET_BINANCE'))


class Command(BaseCommand):
    help = 'Prende gli indici delle candele a '

    def handle(self, *args, **kwargs):
        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        binance_websocket_api_manager.create_stream(['trade', 'kline_1m'], ['btcusdt', 'bnbbtc', 'ethbtc'])

        while True:
            oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
            if oldest_stream_data_from_stream_buffer:
                print(oldest_stream_data_from_stream_buffer)
                unicorn_fied_stream_data = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
