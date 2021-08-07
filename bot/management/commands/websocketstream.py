import datetime
from django.core.management import BaseCommand
import logging
from strategy.models import SymbolExchange
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy
from bot.models import BufferStreamWebSocket

logger = logging.getLogger('main')


class Command(BaseCommand):
    help = 'DispatcherBot'

    def handle(self, *args, **kwargs):

        symbolList = []
        for symbol in SymbolExchange.objects.all():
            symbolList.append(symbol.symbol.lower())

        klines = ['kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_2h', 'kline_4h',
                  'kline_6h', 'kline_8h', 'kline_12h', 'kline_1d', 'kline_3d', 'kline_1w', 'kline_1M']

        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        binance_websocket_api_manager.create_stream(klines, symbolList, output="UnicornFy")

        try:
            while True:

                oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
                if oldest_stream_data_from_stream_buffer:
                    binance_stream = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)

                    BufferStreamWebSocket.objects.filter(
                        created_at__lte=datetime.datetime.now() - datetime.timedelta(minutes=2)).delete()

                    for k, v in binance_stream.items():
                        if isinstance(v, dict):
                            BufferStreamWebSocket.objects.create(
                                symbol=SymbolExchange.objects.get(symbol=v.get('symbol')),
                                time_frame=v.get('interval'),
                                close_candle=float(v.get('close_price')),
                                open_candle=float(v.get('open_price')),
                                high_candle=float(v.get('high_price')),
                                low_candle=float(v.get('low_price')),
                                is_closed=v.get('is_closed')
                            )

        except Exception as e:
            print(e)
            return e
