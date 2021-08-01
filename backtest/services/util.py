from dateutil.relativedelta import relativedelta

from analytics.models import Importer


def find_prev_candle(item):
    now_prev = None
    now = item['timestamp']

    if item['time_frame'] == '1m':
        now_prev = item['timestamp'] - relativedelta(minutes=1)
    if item['time_frame'] == '5m':
        now_prev = item['timestamp'] - relativedelta(minutes=5)
    if item['time_frame'] == '15m':
        now_prev = item['timestamp'] - relativedelta(minutes=15)
    if item['time_frame'] == '30m':
        now_prev = item['timestamp'] - relativedelta(minutes=30)
    if item['time_frame'] == '15m':
        now_prev = item['timestamp'] - relativedelta(minutes=15)
    if item['time_frame'] == '1h':
        now_prev = item['timestamp'] - relativedelta(hours=1)
    if item['time_frame'] == '2h':
        now_prev = item['timestamp'] - relativedelta(hours=2)
    if item['time_frame'] == '4h':
        now_prev = item['timestamp'] - relativedelta(hours=4)
    if item['time_frame'] == '8h':
        now_prev = item['timestamp'] - relativedelta(hours=8)
    if item['time_frame'] == '12h':
        now_prev = item['timestamp'] - relativedelta(hours=12)
    if item['time_frame'] == '1d':
        now_prev = item['timestamp'] - relativedelta(days=1)
    if item['time_frame'] == '3d':
        now_prev = item['timestamp'] - relativedelta(days=3)
    if item['time_frame'] == '1M':
        now_prev = item['timestamp'] - relativedelta(months=1)

    return Importer.objects.filter(symbol=item['symbol'],
                                   tf=item['time_frame'],
                                   timestamp__range=[now_prev, now]) \
        .first()
