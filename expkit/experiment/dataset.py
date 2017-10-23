import numpy as np


class Dataset(object):
    def __init__(self, X, y, feature_names=None):
        self.X = X
        self.y = y
        if feature_names is not None:
            self.feature_names = feature_names
        else:
            self.feature_names = list(range(len(X[0])))

    def merge(self, other):
        self.X = np.concatenate((self.X, other.X), axis=0)
        self.y = np.concatenate((self.y, other.y), axis=0)

