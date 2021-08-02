from analytics.models import ByBt
import datetime


def calculateAvgFromTime(time):
    start_time = datetime.datetime.now().replace(hour=00, minute=00)
    certain_hour = 1
    end_time = start_time.replace(hour=certain_hour)
    qs = ByBt.objects.filter(created_at__range=[start_time, end_time])
    print(qs)
