from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score, confusion_matrix
from ..utils.wrappers import is_wrapper, unwrapped
import numpy as np


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


def apply_classification_metrics(experiment, results):
    results.update({
        "accuracy": accuracy_score(experiment.test_dataset.y, experiment.y_pred),
        "precision": precision_score(experiment.test_dataset.y, experiment.y_pred),
        "recall": recall_score(experiment.test_dataset.y, experiment.y_pred),
        "f1_score": f1_score(experiment.test_dataset.y, experiment.y_pred),
        "confusion_matrix": confusion_matrix(experiment.test_dataset.y, experiment.y_pred),
    })


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
