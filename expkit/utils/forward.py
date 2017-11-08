class MethodForwarder(object):
    def __init__(self, method_name, *args, **kwargs):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs


    def __call__(self, subject, *args, **kwargs):
        return getattr(subject, self.method_name)(*self.args, *args, **self.kwargs, **kwargs)


class AttributeForwarder(MethodForwarder):
    def __init__(self, *args, **kwargs):
        super().__init__("__getattribute__", *args, **kwargs)


class ForwardingPipeline(object):
    def __init__(self, pipeline, *args, **kwargs):
        self.pipeline = pipeline
        self.args = args
        self.kwargs = kwargs


    def __call__(self, subject, *args, **kwargs):
        subject_ = subject
        for element in self.pipeline:
            subject_ = element(subject_, *self.args, *args, **self.kwargs, **kwargs)
        return subject_
