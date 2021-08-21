import decouple
from django.core.management import BaseCommand
import logging
from strategy.models import SymbolExchange
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy
from bot.models import BufferRecordData
import redis

logger = logging.getLogger('main')
import json


class Command(BaseCommand):
    help = 'WebSocketStream Binance'

    def handle(self, *args, **kwargs):

        r = redis.Redis(host=decouple.config('REDIS_HOST'), port=6379, db=0)

        symbolList = []
        for symbol in SymbolExchange.objects.all():
            symbolList.append(symbol.symbol.lower())

        klines = ['kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_2h', 'kline_4h', 'kline_6h',
                  'kline_8h', 'kline_12h', 'kline_1d', 'kline_3d', 'kline_1w', 'kline_1M']

        binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
        binance_websocket_api_manager.create_stream(klines, symbolList, output="UnicornFy")

        while True:
            try:
                oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
                if oldest_stream_data_from_stream_buffer:
                    binance_stream = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
                    for k, v in binance_stream.items():
                        if isinstance(v, dict):

                            candle_is_close =   v.get('is_closed')
                            symbol =            v.get('symbol')
                            interval =          v.get('interval')

                            # Candle not closed - save to redis
                            key = str(SymbolExchange.objects.get(symbol=symbol)) + "_" + str(interval)
                            values = {
                                'candle_close': float(v.get('close_price')),
                                'candle_open': float(v.get('open_price')),
                                'candle_high': float(v.get('high_price')),
                                'candle_low': float(v.get('low_price')),
                                'candle_is_closed': v.get('is_closed'),
                            }
                            r.set(key, json.dumps(values))

                            qs = BufferRecordData.objects.filter(key=key).order_by('created_at')
                            if qs.count() >= 365:
                                qs.first().delete()

                            if qs.count() <= 365:
                                BufferRecordData.objects.create(
                                    key=key,
                                    symbol=symbol,
                                    time_frame=interval,
                                    open_candle=float(v.get('open_price')),
                                    close_candle=float(v.get('close_price')),
                                    high_candle=float(v.get('high_price')),
                                    low_candle=float(v.get('low_price')),
                                    is_closed=candle_is_close,
                                    unix=v.get('kline_start_time'),
                                    volume=v.get('base_volume')
                                )

                            # Candle closed - save to db
                            if candle_is_close:

                                close_candle = float(v.get('close_price'))
                                open_candle = float(v.get('open_price'))
                                high_candle = float(v.get('high_price'))
                                low_candle = float(v.get('low_price'))
                                candle_is_close = v.get('is_closed')
                                symbol = v.get('symbol')
                                interval = v.get('interval')

                                qs = BufferRecordData.objects.filter(key=key).order_by('created_at')

                                if qs.count() >= 365:
                                    qs.first().delete()

                                if qs.count() <= 365:
                                    BufferRecordData.objects.create(
                                            key=key,
                                            symbol=symbol,
                                            time_frame=interval,
                                            open_candle=open_candle,
                                            close_candle=close_candle,
                                            high_candle=high_candle,
                                            low_candle=low_candle,
                                            is_closed=candle_is_close,
                                            unix=v.get('kline_start_time'),
                                            volume=v.get('base_volume')
                                        )

            except Exception as e:
                print(e)
                continue
