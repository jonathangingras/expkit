from .utils.expando import Expando


class Config(Expando):
    USER_ADDED_PREFIX = "user_added__"

    def __init__(self,
                 python="python",
                 latex="pdflatex",
                 result_dir="__results__",
                 experiments_cfg="experiments.py",
                 results_cfg="results.py",
                 open_cmd="open",
                 target="document.pdf",
                 **kwargs):
        for key, val in filter(lambda key_val: id(key_val[1]) != id(self) and id(key_val[1]) != id(kwargs), locals().items()):
            self[key] = val
        for key, val in kwargs.items():
            self[Config.USER_ADDED_PREFIX + key] = val


    def __getattribute__(self, key):
        val = Expando.__getattribute__(self, str(key))
        if val is None:
            return Expando.__getattribute__(self, Config.USER_ADDED_PREFIX + str(key))
        return val


    @staticmethod
    def from_dict(dict_object):
        return Config(**dict_object)


    @staticmethod
    def from_list(list_object):
        return Config.from_dict({key.lower().strip(): val.strip() for key, val in map(lambda el: el.split("="), list_object)})


    @staticmethod
    def from_file(file_object):
        return Config.from_list(list(filter(lambda line: line != '', map(lambda line: line.strip(), file_object.readlines()))))


    @staticmethod
    def from_configfile(filepath="config.expkit"):
        return Config.from_file(open(filepath, "r"))
