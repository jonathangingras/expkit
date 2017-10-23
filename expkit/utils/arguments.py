from sklearn.model_selection import GridSearchCV


class star_wrap(object):
    def __init__(self, function, *additional_args):
        self.function = function
        self.additional_args = additional_args

    def __call__(self, args):
        if isinstance(args, list) or isinstance(args, tuple):
            return self.function(*args, *self.additional_args)
        else:
            return self.function(args, *self.additional_args)
