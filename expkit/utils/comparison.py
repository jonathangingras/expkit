import numpy as np
import sklearn.metrics.scorer


def compare_np_arrays(array1, array2, class_dict):
    return (array1 == array2).all()


def compare_scorers(scorer1, scorer2, _):
    return scorer1._score_func == scorer2._score_func


def compare_dicts(dict1, dict2, class_dict):
    return _DeepComparisonProxy._DeepComparisonProxy__as_proxy_dict(dict1.items(), class_dict) == \
        _DeepComparisonProxy._DeepComparisonProxy__as_proxy_dict(dict2.items(), class_dict)


class _DeepComparisonProxy(object):
    def __init__(self, obj, class_dict):
        self.obj = obj
        self.class_dict = class_dict

    @staticmethod
    def __as_proxy_dict(dict_object, class_dict):
        return {_DeepComparisonProxy(key, class_dict): _DeepComparisonProxy(val, class_dict) \
                for key, val in dict_object}

    def __hash__(self):
        return self.obj.__hash__()

    def __eq__(self, other):
        if self.obj.__class__ == other.obj.__class__:
            if self.obj.__class__ in self.class_dict.keys():
                return self.class_dict[self.obj.__class__](self.obj, other.obj, self.class_dict)

            if callable(getattr(self.obj, "__dict__", None)):
                return _DeepComparisonProxy.__as_proxy_dict(vars(self.obj).items(), self.class_dict) == \
                    _DeepComparisonProxy.__as_proxy_dict(vars(other.obj).items(), self.class_dict)
            else:
                return self.obj == other.obj

        return False


class DeepComparison(object):
    def __init__(self, obj1, obj2, class_dict={}):
        default_class_dict = {
            dict : compare_dicts,
            np.ndarray : compare_np_arrays,
            sklearn.metrics.scorer._PredictScorer : compare_scorers
        }
        default_class_dict.update(class_dict)

        self.proxy1 = _DeepComparisonProxy(obj1, default_class_dict)
        self.proxy2 = _DeepComparisonProxy(obj2, default_class_dict)

    def __bool__(self):
        return self.proxy1 == self.proxy2
