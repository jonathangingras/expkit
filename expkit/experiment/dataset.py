import numpy as np


def arrays_have_same_length(*arrays):
    return len(arrays) == list(map(len, arrays)).count(len(arrays[0]))


def shuffle_arrays(*arrays, seed=None):
    random_state = np.random.RandomState(seed)
    permutations = random_state.permutation(len(arrays[0]))

    if not arrays_have_same_length(*arrays):
        raise RuntimeError("arrays are not all of the same length")

    for i in range(len(arrays)):
        np.take(arrays[i], permutations, axis=0, out=arrays[i])

    if len(arrays) == 1:
        return arrays[0]
    else:
        return arrays


def split_arrays_by_amounts(amount1, amount2, *arrays):
    if not arrays_have_same_length(*arrays):
        raise RuntimeError("arrays are not all of the same length")
    if len(arrays[0]) != amount1 + amount2:
        raise RuntimeError("splitting by amounts require the two amounts to sum to original length")

    def split_array(array):
        return (array[:amount1], array[amount1:])

    if len(arrays) == 1:
        return split_array(arrays[0])
    else:
        return tuple(map(split_array, arrays))


def amounts_from_ratio(ratio, total):
    amount1 = round(ratio * total)
    amount2 = total - amount1
    return amount1, amount2


def split_arrays_by_ratio(ratio, *arrays):
    if not arrays_have_same_length(*arrays):
        raise RuntimeError("arrays are not all of the same length")

    amount1, amount2 = amounts_from_ratio(ratio, len(arrays[0]))

    return split_arrays_by_amounts(amount1, amount2, *arrays)


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
        amount1, amount2 = amounts_from_ratio(ratio, len(self.y))

        return self.split_by_amounts(amount1, amount2)


    def split_by_amounts(self, amount1, amount2):
        (X0, X1), (y0, y1) = split_arrays_by_amounts(amount1, amount2, self.X, self.y)
        return (Dataset(X0, y0, self.feature_names),
                Dataset(X1, y1, self.feature_names))


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
