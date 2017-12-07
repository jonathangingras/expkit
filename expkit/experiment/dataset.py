import numpy as np


class Dataset(object):
    def __init__(self, X, y, feature_names=None, copy=True, X_dtype=None, y_dtype=None):
        if len(X) != len(y):
            raise RuntimeError("first dimension of X and y must be the same")

        if feature_names is not None:
            if len(feature_names) != len(X[0]):
                raise RuntimeError("second dimension of X and amount of feature names must match")
            self.feature_names = feature_names
        else:
            self.feature_names = list(range(len(X[0])))

        self.X = np.array(X, dtype=X_dtype, copy=copy)
        self.y = np.array(y, dtype=y_dtype, copy=copy)


    def shuffle(self, seed=None):
        random_state = np.random.RandomState(seed)
        permutations = random_state.permutation(len(self.X))
        np.take(self.X, permutations, axis=0, out=self.X)
        np.take(self.y, permutations, axis=0, out=self.y)

        return self


    def merge(self, other):
        if (self.X.shape[1] != other.X.shape[1]) or (self.y.shape[1] != other.y.shape[1]) or (self.feature_names != other.feature_names):
            raise RuntimeError("datasets are not compatible either in shape or feature names")

        self.X = np.concatenate((self.X, other.X), axis=0)
        self.y = np.concatenate((self.y, other.y), axis=0)

        return self


    def split(self, ratio=None, amounts=(None, None)):
        if not ratio:
            return self.split_by_amounts(amounts[0], amounts[1])
        else:
            return self.split_by_ratio(ratio)


    def split_by_ratio(self, ratio):
        amount1 = int(ratio * len(self.X))
        amount2 = len(self.X) - amount1

        return self.split_by_amounts(amount1, amount2)


    def split_by_amounts(self, amount1, amount2):
        if len(self.X) != amount1 + amount2:
            raise RuntimeError("splitting by amounts require the two amounts to sum to original length")

        return (Dataset(self.X[:amount1], self.y[:amount1], self.feature_names),
                Dataset(self.X[amount1:], self.y[amount1:], self.feature_names))


class DatasetAbstractSplitMixin(object):
    def __init__(self, X, y, feature_names=None, **dataset_kwargs):
        self.splits = {
            "train": None,
            "test": None,
            "validation": None
        }
        self._split(X, y, feature_names, **dataset_kwargs)


    @classmethod
    def from_dataset(cls, dataset, *args, **kwargs):
        return cls(dataset.X, dataset.y, dataset.feature_names, *args, **kwargs)


    def __getitem__(self, key):
        return self.splits[key]


    def keys(self):
        return self.splits.keys()


class DatasetRandomSplit(DatasetAbstractSplitMixin):
    def __init__(self, *args, ratios={"train-test": 2/3, "train-valid": 2/3}, seed=None, **kwargs):
        self.ratios = ratios
        self.seed = seed
        super().__init__(*args, **kwargs)


    def _split(self, X, y, feature_names=None, **dataset_kwargs):
        data = Dataset(X, y, feature_names, **dataset_kwargs).shuffle(self.seed)
        train, test = data.split(self.ratios["train-test"])
        train, validation = train.split(self.ratios["train-valid"])
        self.splits.update({
            "train": train,
            "test": test,
            "validation": validation
        })
