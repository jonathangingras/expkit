from .operators import unwrapped


class Event(object):
    def __init__(self, callee, *args, **kwargs):
        self.callee = callee
        self.args = args
        self.kwargs = kwargs

    def __call__(self, emitter, *args, **kwargs):
        return self.callee(emitter, *self.args, *args, **self.kwargs, **kwargs)


class EventRegistry(object):
    def __init__(self, emitter):
        self.emitter = emitter
        self.events = {}


    def register_event(self, name, event):
        if name in self.events:
            self.events[name].append(event)
        else:
            self.events.update({name: [event]})


    def emit(self, name, *args, **kwargs):
        result = tuple()

        if name in self.events.keys():
            result = tuple(map(lambda event: event(self.emitter, *args, **kwargs), self.events[name]))
            del self.events[name]

        return result


class LearnerWrapper(object):
    def __init__(self, estimator_class, *args, **kwargs):
        self.estimator_class = estimator_class
        self.args = args
        self.kwargs = kwargs
        self.events = EventRegistry(self)

        self.wrapped = None

        self.after_init()


    def after_init(self):
        self.events.register_event("unwrap", Event(lambda emitter: self.instantiate_estimator()))


    def register_event(self, name, event):
        self.events.register_event(name, event)


    def __is_wrapper__(self):
        return True


    def __wrapped__(self):
        self.events.emit("unwrap")
        return self.wrapped


    def instantiate_estimator(self, *args, **kwargs):
        if self.wrapped is None:
            self.events.emit("instantiation")
            self.wrapped = self.estimator_class(*self.args, *args, **self.kwargs, **kwargs)


    def fit(self, X, y):
        learner = unwrapped(self)
        self.events.emit("fit")
        return learner.fit(X, y)


    def predict(self, X):
        self.events.emit("predict")
        return unwrapped(self).predict(X)

