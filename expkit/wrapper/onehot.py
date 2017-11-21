import numpy as np
from ..utils.conversion import collect_classes, labels_to_one_hots
from .learner import LearnerWrapper, unwrapped


class OneHotClassifierDecorator(object):
    def __init__(self, learner, emitter=None):
        self.learner = learner
        self.emitter = emitter
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
        y = labels_to_one_hots(y, self._classes, dtype=np.float32)

        return self.learner.fit(X, y)


    def predict(self, X):
        y_pred = self.learner.predict(X)

        return np.array(tuple(map(lambda one_hot: self._classes[np.argmax(one_hot[0])], y_pred)))


class OneHotClassifierWrapper(LearnerWrapper):
    def instantiate_estimator(self, *args, **kwargs):
        if self.wrapped is None:
            self.events.emit("instantiation")
            self.wrapped = OneHotClassifierDecorator(self.estimator_class(*self.args, *args, **self.kwargs, **kwargs), self)


    def collect_classes(self, y):
        ret = unwrapped(self).collect_classes(y)
        return ret


    def get_classes(self):
        return unwrapped(self).get_classes()
