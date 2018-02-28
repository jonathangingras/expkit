from time import gmtime, strftime, mktime, struct_time
import calendar
from datetime import datetime
from dateutil import tz


class TimeDelta(object):
    def __init__(self, total_seconds):
        self.total_seconds = int(total_seconds)


    @property
    def total_hours(self):
        return self.total_seconds // 3600


    @property
    def total_minutes(self):
        return self.total_seconds // 60


    @property
    def hours(self):
        return self.total_hours


    @property
    def minutes(self):
        return (self.total_seconds % 3600) // 60


    @property
    def seconds(self):
        return (self.total_seconds % 3600) % 60


    def __str__(self):
        return "Time interval: {} hours, {} mins, {} secs".format(self.hours, self.minutes, self.seconds)


    def __repr__(self):
        return "<TimeDelta: '{}'>".format(str(self))


    def __format__(self, f):
        return str(self)


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


    def __sub__(self, other):
        if(not isinstance(other, Time)):
            raise RuntimeError("other must be a {} object too".format(self.__class__.__name__))
        return TimeDelta((self.get_datetime() - other.get_datetime()).total_seconds())


    def __str__(self):
        return str(self.get_datetime())


    def __repr__(self):
        return "<Time: {}>".format(str(self))


    def __format__(self, f):
        return strftime("%Y_%m_%d__%H_%M_%S", self.get_datetime().timetuple())
