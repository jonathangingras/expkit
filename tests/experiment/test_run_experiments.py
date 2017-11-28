from unittest import TestCase
import os, shutil
from expkit.experiment.shortcuts import run_experiments
from expkit.experiment import Dataset
from sklearn.datasets import load_iris
from sklearn.ensemble import AdaBoostClassifier


class GlobalAccessor(object):
    learner_ = None


    @staticmethod
    def set_learner(learner):
        GlobalAccessor.learner_ = learner


    @staticmethod
    def get_learner():
        return GlobalAccessor.learner_


    @staticmethod
    def clear():
        GlobalAccessor.learner_ = None


class DummyClassifier(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.X = None
        self.y = None

        GlobalAccessor.set_learner(self)


    def fit(self, X, y):
        self.X = X
        self.y = y


    def predict(self, X):
        pass


data = {
    "iris": {
        "train": Dataset(load_iris().data[:100], load_iris().target[:100], load_iris().feature_names),
        "test": Dataset(load_iris().data[100:], load_iris().target[100:], load_iris().feature_names)
    }
}

learners = {
    "Dummy": {
        "class": DummyClassifier,
        "params": {
            "lr": 0.1,
            "someparam": 42
        }
    }
}


class RunExperimentsTest(TestCase):
    def tearDown(self):
        if os.path.exists("__results__"):
            shutil.rmtree("__results__")

        GlobalAccessor.clear()


    def test_instanciates_learner_with_given_params(self):
        run_experiments(data, learners)

        self.assertIsNotNone(GlobalAccessor.get_learner())
        self.assertEqual(learners["Dummy"]["params"], GlobalAccessor.get_learner().kwargs)


    def test_fits_learner_with_train_data(self):
        run_experiments(data, learners)

        self.assertEqual(data["iris"]["train"].X.all(), GlobalAccessor.get_learner().X.all())
        self.assertEqual(data["iris"]["train"].y.all(), GlobalAccessor.get_learner().y.all())

