import numpy as np
from sklearn.model_selection import train_test_split, PredefinedSplit
from .cv import CVWrapper
from ..experiment.dataset import Dataset


class TrainValidationCVWrapper(CVWrapper):
    def __init__(self, estimator_class, *args, **kwargs):
        self.estimator_class = estimator_class
        self.args = args
        self.kwargs = kwargs


    def create_predefined_split(self, train_dataset, validation_dataset):
        train_split = -1 * np.ones(train_dataset.X.shape[0])
        test_split = np.zeros(validation_dataset.X.shape[0])
        split = np.append(train_split, test_split)
        return PredefinedSplit(split)


    def fit(self, X, y):
        train = Dataset(X["train"], y["train"], X["feature_names"])
        valid = Dataset(X["valid"], y["valid"], X["feature_names"])
        alldata = train.merge(valid)

        super().__init__(self.estimator_class, *self.args, cv=self.create_predefined_split(train, valid), **self.kwargs)
        super().fit(alldata.X, alldata.y)



def wrap_train_valid_datasets(train, valid, treatment_train=None, treatment_valid=None):
    if treatment_train:
        train = treatment_train(train)
    if treatment_valid:
        valid = treatment_valid(valid)

    return {
        "X": {"train": train.X, "valid": valid.X, "feature_names": train.feature_names},
        "y": {"train": train.y, "valid": valid.y},
        "feature_names": train.feature_names
    }
