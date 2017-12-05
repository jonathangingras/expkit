import numpy as np
from ..utils.conversion import collect_classes, labels_to_one_hots
from .learner import LearnerWrapper, unwrapped


class OneHotClassifierDecorator(object):
    def __init__(self, learner, emitter=None, y_dtype=None):
        self.learner = learner
        self.emitter = emitter
        self.y_dtype = y_dtype
        self._classes = None


    def collect_classes(self, y):
        if self._classes is None:
            self._classes = collect_classes(y)
            if self.emitter is not None:
                self.emitter.events.emit("classes_collected")


    def get_classes(self):
        return self._classes


    def fit(self, X, y):
        self.collect_classes(y)
        y = labels_to_one_hots(y, self._classes, dtype=self.y_dtype)

        return self.learner.fit(X, y)


    def predict(self, X):
        y_pred = self.learner.predict(X)
        y_pred = y_pred.reshape((y_pred.shape[0], -1))

        return np.array(tuple(map(lambda one_hot: self._classes[np.argmax(one_hot)], y_pred)))


class OneHotClassifierWrapper(LearnerWrapper):
    def __init__(self, estimator_class, *args, y_dtype=None, **kwargs):
        self.y_dtype = y_dtype
        super().__init__(estimator_class, *args, **kwargs)


    def instantiate_estimator(self, *args, **kwargs):
        if self.wrapped is None:
            self.events.emit("instantiation")
            self.wrapped = OneHotClassifierDecorator(self.estimator_class(*self.args, *args, **self.kwargs, **kwargs), emitter=self, y_dtype=self.y_dtype)


    def collect_classes(self, y):
        ret = unwrapped(self).collect_classes(y)
        return ret


    def get_classes(self):
        return unwrapped(self).get_classes()
