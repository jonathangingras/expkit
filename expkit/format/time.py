from time import gmtime, strftime


class Time(object):
    def __init__(self, time_t=gmtime()):
        self.utc_time_t = time_t


    def __str__(self):
        return strftime("%Y-%m-%d_%H.%M.%S", self.utc_time_t)
