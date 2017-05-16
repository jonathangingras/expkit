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


if __name__ == "__main__":
    obj = Expando(_89='opm', kiki=9)
    obj2 = Expando.from_dict({89:'opm2', 'kiki':90})
    print(vars(obj2))

    print(vars(obj))

    for k, v in obj:
        print(str(k) + " : " + str(v))

    print(obj[0])
    obj[0] = 0
    print(obj[0])

    print(obj['_89'])

    obj['_90'] = 90

    print(obj._90)

    obj._91 = 91

    print(vars(obj))
