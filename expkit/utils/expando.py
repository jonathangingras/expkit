class Expando(object):
    def __init__(self, **args):
        for arg in args:
            self.__setattr__(arg, args[arg])


    @staticmethod
    def from_dict(attributes):
        self = Expando()
        self.__init__(**{str(key): attributes[key] for key in attributes.keys()})
        return self


    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, str(key))
        except:
            return None


    def __setattr__(self, key, value):
        object.__setattr__(self, str(key), value)


    def __getitem__(self, key):
        return Expando.__getattribute__(self, str(key))


    def __setitem__(self, key, value):
        return Expando.__setattr__(self, str(key), value)


    def __iter__(self):
        for key in vars(self):
            yield key, self[str(key)]
