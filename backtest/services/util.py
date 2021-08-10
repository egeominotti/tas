from dateutil.relativedelta import relativedelta

from analytics.models import Importer


def find_prev_candle(item, minutes, backtrack):
    """
    :param item:
    :param backtrack:
    :return: Return value of past candle choosed from backtrack
    """

    now_prev = None
    now = item['timestamp']

    if minutes == '1m':
        now_prev = item['timestamp'] - relativedelta(minutes=1 * backtrack)
    if minutes == '5m':
        now_prev = item['timestamp'] - relativedelta(minutes=5 * backtrack)
    if minutes == '15m':
        now_prev = item['timestamp'] - relativedelta(minutes=15 * backtrack)
    if minutes == '30m':
        now_prev = item['timestamp'] - relativedelta(minutes=30 * backtrack)
    if minutes == '15m':
        now_prev = item['timestamp'] - relativedelta(minutes=15 * backtrack)
    if minutes == '1h':
        now_prev = item['timestamp'] - relativedelta(hours=1 * backtrack)
    if minutes == '2h':
        now_prev = item['timestamp'] - relativedelta(hours=2 * backtrack)
    if minutes == '4h':
        now_prev = item['timestamp'] - relativedelta(hours=4 * backtrack)
    if minutes == '8h':
        now_prev = item['timestamp'] - relativedelta(hours=8 * backtrack)
    if minutes == '12h':
        now_prev = item['timestamp'] - relativedelta(hours=12 * backtrack)
    if minutes == '1d':
        now_prev = item['timestamp'] - relativedelta(days=1 * backtrack)
    if minutes == '3d':
        now_prev = item['timestamp'] - relativedelta(days=3 * backtrack)
    if minutes == '1M':
        now_prev = item['timestamp'] - relativedelta(months=1 * backtrack)

    print(now)
    print(now_prev)
    print(item['symbol'])
    print(item['time_frame'])

    return Importer.objects.filter(symbol=item['symbol'],
                                   tf=item['time_frame'],
                                   timestamp__range=[now_prev, now]) \
        .first()
