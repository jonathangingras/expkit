from .operators import unwrapped


class LearnerWrapper(object):
    def __init__(self, estimator_class, *args, **kwargs):
        self.estimator_class = estimator_class
        self.args = args
        self.kwargs = kwargs

        self.wrapped = None


    def __is_wrapper__(self):
        return True


    def __wrapped__(self):
        if not self.wrapped:
            self.wrapped = self.estimator_class(*self.args, **self.kwargs)
        return self.wrapped


    def fit(self, X, y):
        return unwrapped(self).fit(X, y)


    def predict(self, X):
        return unwrapped(self).predict(X)

