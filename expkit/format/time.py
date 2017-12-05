from time import gmtime, strftime, mktime, struct_time
import calendar
from datetime import datetime
from dateutil import tz


class Time(object):
    def __init__(self, utc_struct_time=None):
        if utc_struct_time is None:
            utc_struct_time = gmtime()
        else:
            if not isinstance(utc_struct_time, struct_time):
                raise RuntimeError("Time must be a time.struct_time")

        self.utc_time = utc_struct_time


    @staticmethod
    def now():
        return Time()


    @staticmethod
    def from_utc_struct_time(utc_struct_time):
        return Time(utc_struct_time)


    @staticmethod
    def from_local_struct_time(local_struct_time):
        return Time(gmtime(mktime(local_struct_time)))


    def get_datetime(self):
        return datetime.fromtimestamp(calendar.timegm(self.utc_time))


    def __format__(self, f):
        return strftime("%Y_%m_%d__%H_%M_%S", self.get_datetime().timetuple())


    def __str__(self):
        return str(self.get_datetime())


    def __repr__(self):
        return str(self)
