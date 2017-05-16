from sklearn.model_selection import GridSearchCV


class star_wrap(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, args):
        if isinstance(args, list) or isinstance(args, tuple):
            return self.function(*args)
        else:
            return self.function(args)


class LearnerWrapper:
    def __init__(self, estimator_class, **kwargs):
        self.wrapped = estimator_class(**kwargs)

    def __is_wrapper__(self):
        return True

    def __wrapped__(self):
        return self.wrapped

    def fit(self, X, y):
        return self.wrapped.fit(X, y)

    def predict(self, X):
        return self.wrapped.predict(X)


def unwrapped(wrapper):
    return wrapper.__wrapped__()

def is_wrapper(obj):
    return callable(getattr(obj, "__is_wrapper__", None)) and (getattr(obj, "__wrapped__", None) is not None)


class CV_Wrapper(LearnerWrapper):
    def __init__(self, estimator_class, cv_strategy_class=GridSearchCV, **kwargs):
        self.wrapped = cv_strategy_class(estimator=estimator_class(), **kwargs)

    @property
    def best_estimator_(self):
        return self.wrapped.best_estimator_

    @property
    def cv_results_(self):
        return self.wrapped.cv_results_

    @property
    def best_score_(self):
        return self.wrapped.best_score_

    @property
    def best_params_(self):
        return self.wrapped.best_params_
