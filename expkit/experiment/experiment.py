import os
import pickle as pkl
import numpy as np
from time import gmtime, strftime
import inspect
from sklearn.metrics import accuracy_score, fbeta_score, recall_score, precision_score, confusion_matrix, f1_score
from ..utils.comparison import DeepComparison
from ..utils.wrappers import star_wrap, is_wrapper, unwrapped
from ..utils.iterators import each
from .result_producers import save_learner_object, apply_classification_metrics, apply_feature_names, apply_cv_results


class Dataset(object):
    def __init__(self, X, y, feature_names=None):
        self.X = X
        self.y = y
        if feature_names is not None:
            self.feature_names = feature_names
        else:
            self.feature_names = list(range(len(X[0])))


def _experiment_time():
    return strftime("%Y-%m-%d_%H.%M.%S", gmtime())


class Experiment(object):
    def __init__(self,
                 label,
                 train_dataset,
                 test_dataset,
                 configs=None,
                 output_dir=None,
                 *args,
                 **kwargs):
        if not inspect.isclass(configs["class"]):
            raise RuntimeError("learner_class parameter must be a class fitting sklearn interface")

        self.label = label
        self.learner_class = configs["class"]
        self.train_dataset = train_dataset
        self.test_dataset = test_dataset
        self.configs = {
            "class": self.learner_class.__name__,
            "params": configs["params"]
        }
        if "producers" in configs.keys():
            self.configs["producers"] = configs["producers"]
        else:
            self.configs["producers"] = []

        self.output_dir = output_dir

        self.results = None
        self.producers = [
            save_learner_object,
            apply_feature_names
        ]
        for producer in self.configs["producers"]:
            self.producers.append(producer)

        self.args = args
        self.kwargs = kwargs


    def produce_results(self):
        begin_time = _experiment_time()
        self.learner = self.learner_class(*self.args, **self.kwargs)
        self.learner.fit(self.train_dataset.X, self.train_dataset.y)
        self.y_pred = self.learner.predict(self.test_dataset.X)

        results = {
            "experiment_label": self.label,
            "begin_time": begin_time,
            "finish_time": _experiment_time(),
            "configs": self.configs,
        }

        each(self.producers)(lambda producer: producer(self, results))
        return results


    def result_filepath(self):
        return os.path.join(self.output_dir,
                            self.label.replace(" ", "_") + ".experiment.pkl")


    def __load_existing_results(self):
        if os.path.exists(self.result_filepath()):
            print("already exists")
            with open(self.result_filepath(), "rb") as f:
                try:
                    res = pkl.load(f)
                    if DeepComparison(self.configs, res["configs"]):
                        print("up-to-date pkl")
                        return res
                    else:
                        print("rerunning experiment with new configs")
                except:
                    print("corrupted pickle")
        else:
            print("no existing pkl for " + self.label)


    def __call__(self):
        self.results = self.__load_existing_results()
        if self.results is None:
            self.results = self.produce_results()
        return self.results


    def save_results(self, lazy=True):
        self()
        with open(self.result_filepath(), "wb") as f:
            pkl.dump(self.results, f)


def __all_not_NoneType(*args):
    for element in args:
        if isinstance(element, None.__class__):
            return False
    return True


def __get_valid_dataset(dict_contained_object):
    if __all_not_NoneType(getattr(dict_contained_object, "X", None),
                          getattr(dict_contained_object, "y", None),
                          getattr(dict_contained_object, "feature_names", None)):
        return dict_contained_object
    if isinstance(dict_contained_object, dict):
        return Dataset(dict_contained_object["X"],
                       dict_contained_object["y"],
                       dict_contained_object["feature_names"])
    if callable(dict_contained_object):
        return __get_valid_dataset(dict_contained_object())
    raise RuntimeError("Invalid object passed as dataset")


def __do_experiment(output_dir, data, learners, learner_label, dataset):
    try:
        other_params = learners[learner_label]["params"]
        configs = learners[learner_label]
    except:
        other_params = {}
        configs = dict(params={}, **learners[learner_label])

    Experiment(learner_label + '__' + dataset,
               __get_valid_dataset(data[dataset]['train']),
               __get_valid_dataset(data[dataset]['test']),
               configs=configs,
               output_dir=output_dir,
               **other_params).save_results()


def run_experiments(data, learners, output_dir='__results__', rejected_combinations=()):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    combinations = []
    for dataset in data.keys():
        for learner in learners.keys():
            combinations.append((output_dir, data, learners, learner, dataset))

    return tuple(map(star_wrap(__do_experiment),
              filter(lambda combination: combination not in rejected_combinations, combinations)))
