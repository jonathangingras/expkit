class LearnerWrapper(object):
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

