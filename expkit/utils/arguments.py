from sklearn.model_selection import GridSearchCV


class star_wrap(object):
    def __init__(self, function, *additional_args):
        self.function = function
        self.additional_args = additional_args

    def __call__(self, args):
        if isinstance(args, list) or isinstance(args, tuple):
            return self.function(*args, *self.additional_args)
        else:
            return self.function(args, *self.additional_args)


# source https://stackoverflow.com/questions/3655842/how-can-i-test-whether-a-variable-holds-a-lambda
def islambda(arg):
  LAMBDA = lambda:0
  return isinstance(arg, type(LAMBDA)) and arg.__name__ == LAMBDA.__name__


def reject_keys(dictionnary, rejected_keys):
  return { key: dictionnary[key] for key in filter(lambda key: key not in rejected_keys, dictionnary.keys()) }


def null_function(*args, **kwargs):
    pass


class FallbackAccessor(object):
    def __init__(self, accessed, fallback):
        self.accessed = accessed
        self.fallback = fallback


    def __getitem__(self, *keys):
        try:
            return self.accessed.__getitem__(*keys)
        except KeyError:
            return self.fallback


def fallback_access(accessed, fallback):
    return FallbackAccessor(accessed, fallback)


def call_if_callable(obj, *args, **kwargs):
    if callable(obj):
        return obj(*args, **kwargs)
    else:
        return obj


def merge_dicts(dict1, dict2=None):
    if dict2 is not None:
        dict1.update(dict2)
    return dict1
