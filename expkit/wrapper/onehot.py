import numpy as np
from ..utils.conversion import collect_classes, labels_to_one_hots
from .learner import LearnerWrapper, unwrapped


class OneHotClassifierWrapper(LearnerWrapper):
    def fit(self, X, y):
        self._classes = collect_classes(y)
        y = labels_to_one_hots(y, self._classes, dtype=np.float32)

        return unwrapped(self).fit(X, y)


    def predict(self, X):
        y_pred = unwrapped(self).predict(X)

        return np.array(tuple(map(lambda one_hot: self._classes[np.argmax(one_hot)], y_pred)))
