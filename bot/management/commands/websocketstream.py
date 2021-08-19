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
    help = 'DispatcherBot'

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

                            key = str(SymbolExchange.objects.get(symbol=v.get('symbol'))) + "_" + str(v.get('interval'))

                            values = {
                                'candle_close': float(v.get('close_price')),
                                'candle_open': float(v.get('open_price')),
                                'candle_high': float(v.get('high_price')),
                                'candle_low': float(v.get('low_price')),
                                'candle_is_closed': v.get('is_closed'),
                            }

                            r.set(key, json.dumps(values))

                            if v.get('is_closed'):
                                BufferRecordData.objects.create(
                                    key=SymbolExchange.objects.get(symbol=v.get('symbol')).symbol + "_" + v.get(
                                        'interval'),
                                    symbol=SymbolExchange.objects.get(symbol=v.get('symbol')).symbol,
                                    time_frame=v.get('interval'),
                                    open_candle=float(v.get('open_price')),
                                    close_candle=float(v.get('close_price')),
                                    high_candle=float(v.get('high_price')),
                                    low_candle=float(v.get('low_price')),
                                    is_closed=v.get('is_closed'),
                                    unix=v.get('kline_start_time'),
                                    volume=v.get('base_volume')
                                )

                            # rsi_dict[key] = 0
                            # upperbandValue = None
                            # middlebandValue = None
                            # lowerbandValue = None
                            # if v.get('is_closed'):
                            #     closes.append(float(v.get('close_price')))
                            #     np_closes = numpy.array(closes)
                            #     if len(closes) > RSI:
                            #         rsi = talib.RSI(np_closes, RSI)
                            #         rsi_dict[key] = rsi[-1]
                            #     if len(closes) > BBANDS:
                            #         upperband, middleband, lowerband = talib.BBANDS(closes, timeperiod=20, nbdevup=2,nbdevdn=2, matype=0)
                            #         upperbandValue = upperband
                            #         bbands = upperband
                            #         bbands = upperband



            except Exception as e:
                print(e)
                continue
