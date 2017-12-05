import os
import pickle as pkl
import inspect
from ..utils.comparison import DeepComparison
from ..utils.iterators import each
from ..utils.arguments import fallback_access, reject_keys, islambda, null_function
from ..format import Time
from .dataset import Dataset
from .result_producers import save_learner_object, apply_feature_names


def assert_not_in_main_module(possible_callable):
    if not callable(possible_callable):
        return possible_callable
    else:
        if not islambda(possible_callable) and possible_callable.__module__ == "__main__":
            raise RuntimeError("A callable living in main module is not pickleable")
        else:
            return possible_callable


def all_not_NoneType(*args):
    for element in args:
        if isinstance(element, None.__class__):
            return False
    return True


def get_valid_dataset(dict_contained_object):
    if all_not_NoneType(getattr(dict_contained_object, "X", None),
                        getattr(dict_contained_object, "y", None),
                        getattr(dict_contained_object, "feature_names", None)):
        return dict_contained_object

    if isinstance(dict_contained_object, dict):
        return Dataset(dict_contained_object["X"],
                       dict_contained_object["y"],
                       dict_contained_object["feature_names"])

    if callable(dict_contained_object):
        return get_valid_dataset(dict_contained_object())

    raise RuntimeError("Invalid object passed as dataset")


class ExperimentSetup(object):
    def __init__(self,
                 label,
                 datasets,
                 configs={}):
        if not inspect.isclass(configs["class"]):
            raise RuntimeError("learner_class parameter must be a class meeting sklearn interface")

        self.label = label
        self.train_dataset = assert_not_in_main_module(datasets["train"])
        self.test_dataset = assert_not_in_main_module(datasets["test"])
        self.dataset_extra_params = reject_keys(datasets, ["train", "test"])
        self.configs = configs

        self.learner = None
        self.y_pred = None
        self.results = None


    def result_producers(self):
        return [
            apply_feature_names,
            save_learner_object
        ] + fallback_access(self.configs, [])["producers"]


    def learner_class(self):
        return self.configs["class"]


    def learner_params(self):
        params = {}
        params.update(fallback_access(self.configs, {})["params"])
        return params


    def saved_configs(self, alt_configs=None):
        configs = alt_configs if alt_configs is not None else self.configs
        return reject_keys(configs, ["unsaved"] + fallback_access(configs, [])["unsaved"])


    def run(self):
        self.learner = self.learner_class()(**self.learner_params())

        self.train_dataset = get_valid_dataset(self.train_dataset)
        self.test_dataset = get_valid_dataset(self.test_dataset)

        fallback_access(self.configs, null_function)["before"](self)

        begin_time = Time()
        self.learner.fit(self.train_dataset.X, self.train_dataset.y)
        self.y_pred = self.learner.predict(self.test_dataset.X)
        finish_time = Time()

        fallback_access(self.configs, null_function)["after"](self)

        results = {
            "experiment_label": self.label,
            "begin_time": begin_time,
            "finish_time": finish_time,
            "configs": self.saved_configs(),
        }

        each(self.result_producers())(lambda producer: producer(self, results))

        return results


    def __load_existing_results(self, already_filled_result_dir):
        if not already_filled_result_dir:
            return None
        if os.path.exists(self.result_filepath(already_filled_result_dir)):
            print("already exists")
            with open(self.result_filepath(already_filled_result_dir), "rb") as f:
                try:
                    res = pkl.load(f)

                    if DeepComparison(self.saved_configs(), self.saved_configs(res["configs"])):
                        print("up-to-date pkl")
                        return res
                    else:
                        print("rerunning experiment with new configs")
                except Exception as error:
                    print(error)
                    print("corrupted pickle")
        else:
            print("no existing pkl for " + self.label)
            return None


    def __call__(self, result_dir=None):
        if not self.results:
            if result_dir:
                self.results = self.__load_existing_results(result_dir)

                if not self.results:
                    self.results = self.run()
                    self.save_results(result_dir)

            else:
                self.results = self.run()

        return self.results


    def output_filepath(self, output_dir):
        return os.path.join(output_dir,
                            self.label.replace(" ", "_") + ".experiment.pkl")


    def result_filepath(self, result_dir):
        return os.path.join(result_dir,
                            self.label.replace(" ", "_") + ".results.pkl")


    def save_results(self, result_dir):
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)

        with open(self.result_filepath(result_dir), "wb") as f:
            pkl.dump(self.results, f)


    def save(self, output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        with open(self.output_filepath(output_dir), "wb") as f:
            pkl.dump(self, f)
