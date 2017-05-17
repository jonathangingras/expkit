class Expando(object):
    def __init__(self, **args):
        for arg in args:
            self.__setattr__(arg, args[arg])

    @staticmethod
    def from_dict(attributes):
        self = Expando()
        self.__init__(**{str(key): attributes[key] for key in attributes.keys()})
        return self

    def __iter__(self):
        for key in vars(self):
            yield key, self.__getattribute__(str(key))

    def __getitem__(self, key):
        try:
            return self.__getattribute__(str(key))
        except:
            return None

    def __setitem__(self, key, value):
        return self.__setattr__(str(key), value)
