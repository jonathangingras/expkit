from time import gmtime, strftime, mktime
import calendar
from datetime import datetime
from dateutil import tz


class Time(object):
    def __init__(self, time_t=gmtime()):
        self.utc_time_t = time_t


    def __str__(self):
        return strftime("%Y-%m-%d_%H.%M.%S", self.utc_time_t)


    def __repr__(self):
        return str(datetime.fromtimestamp(calendar.timegm(self.utc_time_t)))
