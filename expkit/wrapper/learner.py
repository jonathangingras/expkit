from .operators import unwrapped


class Event(object):
    def __init__(self, callee, *args, **kwargs):
        self.callee = callee
        self.args = args
        self.kwargs = kwargs

    def __call__(self, emitter):
        return self.callee(emitter, *self.args, **self.kwargs)


class EventRegistry(object):
    def __init__(self, emitter):
        self.emitter = emitter
        self.events = {}


    def register_event(self, name, event):
        if name in self.events:
            self.events[name].append(event)
        else:
            self.events.update({name: [event]})


    def emit(self, name):
        if name in self.events.keys():
            return tuple(map(lambda event: event(self.emitter), self.events[name]))
        else:
            return tuple()


class LearnerWrapper(object):
    def __init__(self, estimator_class, *args, **kwargs):
        self.estimator_class = estimator_class
        self.args = args
        self.kwargs = kwargs
        self.events = EventRegistry(self)

        self.wrapped = None


    def register_event(self, name, event):
        self.events.register_event(name, event)


    def __is_wrapper__(self):
        return True


    def __wrapped__(self, *args, **kwargs):
        self.events.emit("unwrap")
        if not self.wrapped:
            self.events.emit("estimator_instantiation")
            self.wrapped = self.estimator_class(*args, *self.args, **kwargs, **self.kwargs)
        return self.wrapped


    def fit(self, X, y):
        learner = unwrapped(self)
        self.events.emit("fit")
        return learner.fit(X, y)


    def predict(self, X):
        self.events.emit("predict")
        return unwrapped(self).predict(X)

