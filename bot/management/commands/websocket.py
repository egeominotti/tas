from django.core.management import BaseCommand
import logging
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'DispatcherBot'

    def handle(self, *args, **kwargs):

        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        binance_websocket_api_manager.create_stream(['kline_1m'], ['btcusdt'],output="UnicornFy")

        try:
            while True:

                oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
                if oldest_stream_data_from_stream_buffer:
                    binance_stream = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
                    for k, v in binance_stream.items():
                        if isinstance(v, dict):
                            # v.get('open_price')
                            # v.get('close_price')
                            # v.get('low_price')
                            # v.get('high_price')
                            # v.get('is_closed')
                            print(float(v.get('close_price')))

        except Exception as e:
            return e
