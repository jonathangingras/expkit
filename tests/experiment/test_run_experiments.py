from unittest import TestCase
import os, shutil
from expkit.experiment.shortcuts import run_experiments
from expkit.experiment import Dataset
from expkit.utils.arguments import reject_keys
from sklearn.datasets import load_iris
from sklearn.ensemble import AdaBoostClassifier


class Accessor(object):
    def __init__(self):
        self.learner_ = None


    def set_learner(self, learner):
        self.learner_ = learner


    def get_learner(self):
        return self.learner_


    def __eq__(self, other):
        return True


    def clear(self):
        self.learner_ = None


class DummyClassifier(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = reject_keys(kwargs, ["accessor"])
        self.X = None
        self.y = None

        kwargs["accessor"].set_learner(self)


    def fit(self, X, y):
        self.X = X
        self.y = y


    def predict(self, X):
        pass


def get_data():
    return {
        "iris": {
            "train": Dataset(load_iris().data[:100], load_iris().target[:100], load_iris().feature_names),
            "test": Dataset(load_iris().data[100:], load_iris().target[100:], load_iris().feature_names)
        }
    }


def get_learners():
    return {
        "Dummy": {
            "class": DummyClassifier,
            "params": {
                "lr": 0.1,
                "someparam": 42,
                "accessor": Accessor()
            }
        }
    }


def get_accessor(learners):
    return learners["Dummy"]["params"]["accessor"]


class RunExperimentsTest(TestCase):
    RESULT_DIRNAME = "__results__"


    def test_instanciates_learner_with_given_params(self):
        data, learners = get_data(), get_learners()

        run_experiments(data, learners, self.RESULT_DIRNAME + "1")

        self.assertEqual(reject_keys(learners["Dummy"]["params"], ["accessor"]),
                         get_accessor(learners).get_learner().kwargs)
        shutil.rmtree(self.RESULT_DIRNAME + "1")


    def test_fits_learner_with_train_data(self):
        data, learners = get_data(), get_learners()

        run_experiments(data, learners, self.RESULT_DIRNAME + "2")

        self.assertEqual(data["iris"]["train"].X.all(), get_accessor(learners).get_learner().X.all())
        self.assertEqual(data["iris"]["train"].y.all(), get_accessor(learners).get_learner().y.all())
        shutil.rmtree(self.RESULT_DIRNAME + "2")

