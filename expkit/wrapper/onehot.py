import numpy as np
from ..utils.conversion import collect_classes, labels_to_one_hots
from .learner import LearnerWrapper, unwrapped


class OneHotClassifierDecorator(object):
    def __init__(self, learner):
        self.learner = learner
        self._classes = None


    def fit(self, X, y):
        self._classes = collect_classes(y)
        y = labels_to_one_hots(y, self._classes, dtype=np.float32)

        return self.learner.fit(X, y)


    def predict(self, X):
        y_pred = self.learner.predict(X)

        return np.array(tuple(map(lambda one_hot: self._classes[np.argmax(one_hot)], y_pred)))


class OneHotClassifierWrapper(LearnerWrapper):
    def fit(self, X, y):
        self._onehot_decorator = OneHotClassifierDecorator(unwrapped(self))
        return self._onehot_decorator.fit(X, y)


    def predict(self, X):
        return self._onehot_decorator.predict(X)
