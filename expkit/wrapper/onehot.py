import numpy as np
from ..utils.conversion import collect_classes, labels_to_one_hots
from .learner import LearnerWrapper, unwrapped


class OneHotClassifierDecorator(object):
    def __init__(self, learner):
        self.learner = learner
        self._classes = None


    def collect_classes(self, y):
        if self._classes is None:
            self._classes = collect_classes(y)


    def fit(self, X, y):
        self.collect_classes(y)
        y = labels_to_one_hots(y, self._classes, dtype=np.float32)

        return self.learner.fit(X, y)


    def predict(self, X):
        y_pred = self.learner.predict(X)

        return np.array(tuple(map(lambda one_hot: self._classes[np.argmax(one_hot)], y_pred)))


class OneHotClassifierWrapper(LearnerWrapper):
    def instantiate_decorator(self):
        if not getattr(self, "_onehot_decorator", None):
            self._onehot_decorator = OneHotClassifierDecorator(unwrapped(self))


    def collect_classes(self, y):
        self.instantiate_decorator()
        self._onehot_decorator.collect_classes(y)
        self._classes = self._onehot_decorator._classes


    def fit(self, X, y):
        self.instantiate_decorator()
        return self._onehot_decorator.fit(X, y)


    def predict(self, X):
        return self._onehot_decorator.predict(X)
