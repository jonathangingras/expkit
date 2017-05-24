def iterable(obj):
    return callable(getattr(obj, "__iter__", None))


class BaseMixin(object):
    def __init__(self, iterable, except_any=False):
        self.iterable = iterable
        self.except_any = except_any

    def _in_generate(self, i, function, *args, **kwargs):
        try:
            return function(i, *args, **kwargs)
        except Exception as exception:
            if not self.except_any:
                raise exception

    def _iterable(self):
        return self.iterable

    def generate(self, function, *args, **kwargs):
        for i in self._iterable():
            ret = self._in_generate(i, function, *args, **kwargs)
            if ret is not None:
                yield ret

    def __call__(self, function, *args, **kwargs):
        return tuple(self.generate(function, *args, **kwargs))


class each(BaseMixin):
    pass


class on(BaseMixin):
    def __init__(self, iterable, containing, except_any=False):
        super().__init__(iterable, except_any=except_any)
        self.containing = containing

    def _iterable(self):
        return filter(lambda j: str(self.containing) in j, self.iterable)
