from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score, confusion_matrix
from ..wrapper.operators import is_wrapper, unwrapped
import numpy as np
from ..utils.iterators import each


class Producer(object):
    def __init__(self, callable_producer, name=None):
        self.name = name if name else callable_producer.__name__
        self.producer = callable_producer


    def __eq__(self, other):
        return isinstance(other, Producer) and \
            self.name == other.name and \
            self.producer == other.producer


class GlobalExperimentProducer(Producer):
    def __call__(self, experiment, results):
        results.update({
            str(self.name): self.producer(experiment)
        })


class PredictionProducer(Producer):
    def __call__(self, experiment, results):
        results.update({
            str(self.name): self.producer(experiment.test_dataset.y, experiment.y_pred)
        })


class ProducerAggregate(Producer):
    def __init__(self, callable_producers, name):
        self.name = name
        self.producer = callable_producers


    def __call__(self, experiment, results):
        results.update({self.name: {}})
        each(self.producer)(lambda producer: producer(experiment, results[self.name]))


def save_entire_data(experiment, results):
    results.update({
        "y_pred": experiment.y_pred,
        "train_dataset": experiment.train_dataset,
        "test_dataset": experiment.test_dataset
    })


def save_learner_object(experiment, results):
    if is_wrapper(experiment.learner):
        results["learner"] = unwrapped(experiment.learner)
    else:
        results["learner"] = experiment.learner


def apply_common_classification_metrics(experiment, results):
    ProducerAggregate(map(PredictionProducer, [
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
        confusion_matrix
    ]), "classification_metrics")(experiment, results)


def apply_feature_names(experiment, results):
    results.update({"feature_names": experiment.train_dataset.feature_names})


def apply_cv_results(experiment, results):
    results.update({
        "actual_learner": experiment.learner.best_estimator_,
        "cv_results": experiment.learner.cv_results_,
        "best_score": experiment.learner.best_score_,
        "best_params": experiment.learner.best_params_,
    })


def apply_fbetas(experiment, results):
    for beta in np.arange(0.1, 10.1, 0.1):
        results["f_{}".format("{" + str(beta) + "}")] \
            = fbeta_score(experiment.test_dataset.y, experiment.y_pred, beta=beta)
